#include<iostream>
#include<stdlib.h>
#include<math.h>


namespace Echo_vector
{   
    const float Random_coeef_bound = 1.0;
    const float Base_coeef = 0.989789;
    const float Random_coeff = static_cast <float> (rand()) / static_cast<float>(Random_coeef_bound);
    
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


    class Vector_movement_and_rotation
    {
        public:

        //=====================================================================================================
        void object_rotation(int *vector, int vector_size)
        {
            vector[0] = vector[0] * cos(rot_yaw) * cos(rot_roll) - vector[0] * cos(rot_pitch) * sin(rot_yaw) * sin(rot_roll) - vector[0] * cos(rot_roll) * sin(rot_yaw) - vector[0] * cos(rot_yaw) * cos(rot_pitch) * sin(rot_roll) + vector[0] * sin(rot_pitch) * sin(rot_roll);
            vector[1] = vector[1] * cos(rot_pitch) * cos(rot_roll) * sin(rot_yaw) + vector[1] * cos(rot_yaw) * sin(rot_roll) + vector[1] * cos(rot_yaw) * cos(rot_pitch) * cos(rot_roll) - vector[1] * sin(rot_yaw) * sin(rot_roll) - vector[1] * cos(rot_roll) * sin(rot_pitch);
            vector[2] = vector[2] * sin(rot_yaw) * sin(rot_pitch) + vector[2] * cos(rot_yaw) * sin(rot_pitch) + vector[2] * cos(rot_pitch);

        }
        //=====================================================================================================
        void object_movement(int *vector, int vector_size)
        {
            vector[0] = vector[0] + move_x * Base_coeef;
            vector[1] = vector[1] + move_y * Base_coeef;
            vector[2] = vector[2] + move_z * Base_coeef;

        }
        //=====================================================================================================
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
    {
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

        float Tensor_of_inertia[3][3];
        for (int iter_i = 0; iter_i < 3; iter_i ++)
        {
            for (int iter_j = 0; iter_j < 3; iter_j ++)
            {
                if (iter_i == iter_j and iter_i == 1) 
                {
                    Tensor_of_inertia[iter_i][iter_j] = Moment_of_inertia_Ox;
                }
        
                else if (iter_j == iter_i and iter_i == 2)
                {
                    Tensor_of_inertia[iter_i][iter_j] = Moment_of_inertia_Oy;
                }
        
              else if (iter_j == iter_i and iter_i == 3)
              {
                  Tensor_of_inertia[iter_i][iter_j] = Moment_of_inertia_Oz;
              }
          }
        } 


    
    };


}