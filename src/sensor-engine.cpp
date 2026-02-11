#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <nlohmann/json.hpp>
#include <mosquitto.h>


using json = nlohmann::json;


int main(int argc, char* argv[]){

    std::string sensorID = "sensor_01";
    double temperature = 25.5;

    if (argc >= 2) sensorID = argv[1];
    if (argc >= 3) temperature = std::stod(argv[2]);

    mosquitto_lib_init();
  
    struct mosquitto *mosq_client = mosquitto_new(sensorID.c_str(), true, NULL);
    mosquitto_connect(mosq_client, "localhost", 1883, 60);

    json j;
    j["ID"] = sensorID;

    while(true){

        temperature += (25.5 - temperature) * 0.01 + (rand() % 11 - 5) * 0.05;
        j["temperatura"] = std::round(temperature * 100.0)/100;
        std::string leitura = j.dump();

        if(mosquitto_publish(mosq_client, NULL, "sensores/cpp17", leitura.length(), leitura.c_str(), 0, false) != 0){
            std::cerr << "ERRO AO ENVIAR LEITURA AO BROKER" << std::endl;
            return 1;
        }else{
            std::cout << " Enviado com sucesso!\n";
       }
        std::this_thread::sleep_for(std::chrono::seconds(2));
   }

    return 0;
}
