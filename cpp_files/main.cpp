#include<iostream>
#include<stdlib.h>
#include<math.h>


namespace Echo_vector
{   
    const float Random_coeef_bound = 1.0;
    const float Base_coeef = 0.989789;
    const float Random_coeff = static_cast <float> (rand()) / static_cast<float>(Random_coeef_bound);
    
    const float Cooef_of_rotor_B = 12.9898;
    const float Lenght_of_one_part = 6.9898;
    const float Gravity_cooef_G = 9.81;
    const float Differencial_cooef = 0.01;
    
    int *sistem_object_position_array = (int*)malloc(sizeof(int) * 100);
    int *sistem_object_velocity_array = (int*)malloc(sizeof(int) * 100);
    int *sistem_object_acceleration_array = (int*)malloc(sizeof(int) * 100);

    float curent_sistem_position = 0.0;
    float curent_sistem_velocity = 0.0;
    float curent_sistem_acceleration = 0.0;

    float sistem_error = 0;
    float sistem_previous_error = 0;
    int sistem_desired_position = 10;
    float sistem_saturation_limit = 1000.0;
    float pid_integral = 1.0;
   
    float K_p = 0.9898;
    float K_d = 1.9897;
    float K_i = 0.001;


    int copter_rotor_count = 4;
    float copter_angular_velocity = 0.0;
    float copter_angular_velocity_sum = 0;
    float copter_mass = 0.06;

    float rot_pitch = 0.0;
    float rot_roll = 0.0;
    float rot_yaw = 0.0;

    float move_x = 0.0;
    float move_y = 0.0;
    float move_z = 0.0;

    bool move_x_flag = false;
    bool move_y_flag = false;
    bool move_z_flag = false;

    bool rot_pitch_flag = false;
    bool rot_roll_flag = false;
    bool rot_yaw_flag = false;

    int sistem_simulation_episodes = 100;

    class Vector_movement_and_rotation
    {
        public:

            //=====================================================================================================
            // init object coordinate vector rotation
            // simple using rotation eular matrix
            void object_rotation(int *vector, int vector_size)
            {
                vector[0] = vector[0] * cos(rot_yaw) * cos(rot_roll) - vector[0] * cos(rot_pitch) * sin(rot_yaw) * sin(rot_roll) - vector[0] * cos(rot_roll) * sin(rot_yaw) - vector[0] * cos(rot_yaw) * cos(rot_pitch) * sin(rot_roll) + vector[0] * sin(rot_pitch) * sin(rot_roll);
                vector[1] = vector[1] * cos(rot_pitch) * cos(rot_roll) * sin(rot_yaw) + vector[1] * cos(rot_yaw) * sin(rot_roll) + vector[1] * cos(rot_yaw) * cos(rot_pitch) * cos(rot_roll) - vector[1] * sin(rot_yaw) * sin(rot_roll) - vector[1] * cos(rot_roll) * sin(rot_pitch);
                vector[2] = vector[2] * sin(rot_yaw) * sin(rot_pitch) + vector[2] * cos(rot_yaw) * sin(rot_pitch) + vector[2] * cos(rot_pitch);

            }
            //=====================================================================================================
            // init object coordinate vector movement
            // simple using movement matrix
            void object_movement(int *vector, int vector_size)
            {
                vector[0] = vector[0] + move_x * Base_coeef;
                vector[1] = vector[1] + move_y * Base_coeef;
                vector[2] = vector[2] + move_z * Base_coeef;

            }
            //=====================================================================================================
            // init movement flags for directly controlling of movement
            void movement_flags()
            {
                switch (move_x_flag)
                {
                    case true:
                        move_x = move_x * Random_coeef_bound + Base_coeef;
                        std::cout << "distance on x with changes:\t" << move_x << "\n";
                    
                    case false:
                        std::cout << "distance on x:\t" << move_x << "\n";
                }

                switch (move_y_flag)
                {
                    case true:
                        move_y = move_y * Random_coeef_bound + Base_coeef;
                        std::cout << "distance on y with changes:\t" << move_y << "\n";

                    case false:
                        std::cout << "distance on_y:\t" << move_y;
                }

                switch (move_z_flag)
                {
                    case true:
                        move_z = move_z * Random_coeef_bound + Base_coeef;
                        std::cout << "distance on z with changes:\t" << move_z << "\n";
                    
                    case false:
                        std::cout << "distance on z:\t" << move_z << "\n";

                }

                switch (rot_pitch_flag)
                {
                    case true:
                        rot_pitch = rot_pitch * Random_coeef_bound + Base_coeef;
                        std::cout << "angle of pitch with changes:\t" << rot_pitch << "\n";
                    
                    case false:
                        std::cout << "angle of pitch:\t" << rot_pitch << "\n";
                    
                }
                
                switch (rot_roll_flag)
                {
                    case true:
                        rot_roll = rot_roll * Random_coeef_bound + Base_coeef;
                        std::cout << "angle of roll with changes:\t" << rot_roll << "\n";
                    
                    case false:
                        std::cout << "angle of roll:\t" << rot_roll;
                    
                }

                switch (rot_yaw_flag)
                {
                    case true:
                        rot_yaw = rot_yaw * Random_coeef_bound + Base_coeef;
                        std::cout << "angle of yaw with changes:\t" << rot_yaw << "\n";
                    
                    case false:
                        std::cout << "angle of yaw:\t" << rot_yaw << "\n";
                }
            }
            //=========================================================================================
            void change_stats(int *vector, int vector_size)
            {
                movement_flags();
                object_movement(vector, vector_size);
                object_rotation(vector, vector_size);
            }
        
    };

    class Copter_mechanik: private Vector_movement_and_rotation
    {   public:
            float mass_1 = 0.9898;
            float mass_2 = 1.9898;
            float mass_3 = 2.9898;
            float mass = 5.9898;

            float R = 6.9898;
            float r_1 = 1.9898;
            float r_2 = 2.9898;
            float r_3 = 3.9898;

            float Moment_of_inertia_Ox = (2 * mass_1 * pow(r_1, 2)) / 5 + mass * pow(R, 2);
            float Moment_of_inertia_Oy = (2 * mass_2 * pow(r_2, 2)) / 5 + mass * pow(R, 2);
            float Moment_of_inertia_Oz = (1 * mass_3 * pow(r_3, 2)) / 5 + mass * pow(R, 2);

            void init_copter_mech()
            {

                for (int item = 0; item < sizeof(int) * 100; item ++){
                    
                    sistem_object_position_array[item] = 0.0;
                    sistem_object_velocity_array[item] = 0.0;
                    sistem_object_acceleration_array[item] = 0.0;
                }
            }

            void calculate_sistem_acceleration()
            {
                
                for (int item = 0; item < copter_rotor_count; item++){
                    copter_angular_velocity_sum = copter_angular_velocity_sum + copter_angular_velocity;
                }
                curent_sistem_acceleration = (copter_angular_velocity_sum * Cooef_of_rotor_B) / copter_mass - Gravity_cooef_G;

            }
            
            void calculate_sistem_velocity_and_position()
            {

                curent_sistem_velocity += curent_sistem_acceleration * Differencial_cooef;
                curent_sistem_position += curent_sistem_velocity * Differencial_cooef;

            }

            float saturation_limit(float power_U)
            {
                if (power_U > sistem_saturation_limit){
                    return sistem_saturation_limit;
                }
                else if (power_U < -sistem_saturation_limit){
                    return -sistem_saturation_limit;
                }
            }

            void calculate_PID()
            {
                sistem_error = sistem_desired_position - curent_sistem_position;
                pid_integral = sistem_error + sistem_error * Differencial_cooef;
                copter_angular_velocity = K_p * sistem_error + K_i * pid_integral + K_d * (sistem_error - sistem_previous_error) / Differencial_cooef;
                copter_angular_velocity = saturation_limit(copter_angular_velocity);

            }

            void run_sistem_simulation()
            {
                int simulation_counter = 0;
                while (simulation_counter < sistem_simulation_episodes)
                {
                    sistem_object_acceleration_array[simulation_counter] = curent_sistem_acceleration;
                    sistem_object_velocity_array[simulation_counter] = curent_sistem_velocity;
                    sistem_object_position_array[simulation_counter] = curent_sistem_position;
                    std::cout <<"\nSISTEM CURENT ACCELERATION:\t" << curent_sistem_acceleration <<"\tSISTEM CURENT VELOCITY:\t" << curent_sistem_velocity << "\tSISTEM CURENT POSITION:\t" << curent_sistem_position << "\n";
                    calculate_sistem_acceleration();
                    calculate_sistem_velocity_and_position();
                    calculate_PID();

                }
            }
    };


}

int main()
{
    Echo_vector::Copter_mechanik copter;
    copter.init_copter_mech();
    copter.run_sistem_simulation();

    
}