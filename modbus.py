###########  Programa para geração de base de dados, coleta remota de dados #############
###########  via protocolo Modbus TCP/IP e atualização de base de dados.    #############
###########                 Autor:  Flavio Gomes                            #############


## Importação de Pacotes
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import sqlite3
import time

## Criando a base de dados
conn = sqlite3.connect('ammonit.db')
print ('Base de dados ''ammonit'' conectada')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Tabela(ano REAL,mes REAL, dia REAL,hora REAL,minuto REAL,segundo REAL, vel_vento REAL, vel_vento_media REAL,vel_vento_max REAL, vel_vento_min REAL, vel_vento_sdtdev REAL, dir_vento REAL, dir_vento_media REAL, umid_rel REAL, umid_rel_media REAL, umid_rel_max REAL, umid_rel_min REAL, umid_rel_stddev REAL, temp_amb REAL, temp_amb_media REAL, temp_amb_max REAL, temp_amb_min REAL, temp_amb_stddev REAL, pressao_atm REAL, pressao_atm_media REAL, pressao_atm_max REAL, pressao_atm_min REAL, pressao_atm_stddev REAL, DHI REAL, DHI_media REAL, DHI_max REAL, DHI_min REAL, DHI_stddev REAL, GHI REAL, GHI_media REAL, GHI_max REAL, GHI_min REAL, GHI_stddev REAL, DNI REAL, DNI_media REAL, DNI_max REAL, DNI_min REAL, DNI_stddev REAL, DNI_estado_sol REAL, precipitacao REAL, GTI REAL, GTI_media REAL, GTI_max REAL, GTI_min REAL, GTI_stddev REAL, tensao_A REAL, tensao_B REAL, temperatura_A REAL, temperatura_B REAL)')
    print ('Tabela criada na base de dados')

class FloatModbusClient(ModbusClient):
    def read_float(self, address, number=1):
        reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None

    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)


def data_entry():
    # TCP auto connect on first modbus request
    
    # Ler dados
    m = FloatModbusClient(host='localhost', port=502, auto_open=True)
    dados = [
             m.read_holding_registers(101,1),m.read_holding_registers(102,1),
             m.read_holding_registers(103,1),m.read_holding_registers(104,1),
             m.read_holding_registers(105,1),m.read_holding_registers(106,1),
             m.read_holding_registers(1,1),  m.read_holding_registers(3,1),
             m.read_holding_registers(5,1),  m.read_holding_registers(7,1),
             m.read_holding_registers(9,1),  m.read_holding_registers(11,1),
             m.read_holding_registers(13,1), m.read_holding_registers(15,1),
             m.read_holding_registers(17,1), m.read_holding_registers(19,1),
             m.read_holding_registers(21,1), m.read_holding_registers(23,1),
             m.read_holding_registers(25,1), m.read_holding_registers(27,1),
             m.read_holding_registers(29,1), m.read_holding_registers(31,1),
             m.read_holding_registers(33,1), m.read_holding_registers(35,1),
             m.read_holding_registers(37,1), m.read_holding_registers(39,1),
             m.read_holding_registers(41,1), m.read_holding_registers(43,1),
             m.read_holding_registers(45,1), m.read_holding_registers(47,1),
             m.read_holding_registers(49,1), m.read_holding_registers(51,1),
             m.read_holding_registers(53,1), m.read_holding_registers(55,1),
             m.read_holding_registers(57,1), m.read_holding_registers(59,1),
             m.read_holding_registers(61,1), m.read_holding_registers(63,1),
             m.read_holding_registers(65,1), m.read_holding_registers(67,1),
             m.read_holding_registers(69,1), m.read_holding_registers(71,1),
             m.read_holding_registers(73,1), m.read_holding_registers(75,1),
             m.read_holding_registers(77,1), m.read_holding_registers(79,1),
             m.read_holding_registers(81,1), m.read_holding_registers(83,1),
             m.read_holding_registers(85,1), m.read_holding_registers(87,1),
             m.read_holding_registers(89,1), m.read_holding_registers(91,1),
             m.read_holding_registers(93,1), m.read_holding_registers(95,1),
             m.read_holding_registers(97,1)]
    print(dados)
    m.close()

    # Inserção dos dados
    c.execute('INSERT INTO Tabela (ano, mes, dia, hora, minuto, segundo, vel_vento,vel_vento_media, vel_vento_max, vel_vento_min, vel_vento_sdtdev, dir_vento,        dir_vento_media, umid_rel, umid_rel_media, umid_rel_max, umid_rel_min, umid_rel_stddev,temp_amb, temp_amb_media, temp_amb_max, temp_amb_min, temp_amb_stddev, pressao_atm,       pressao_atm_media, pressao_atm_max, pressao_atm_min, pressao_atm_stddev, DHI, DHI_media,   DHI_max, DHI_min, DHI_stddev, GHI, GHI_media, GHI_max, GHI_min, GHI_stddev, DNI,    DNI_media, DNI_max, DNI_min, DNI_stddev, DNI_estado_sol, precipitacao, GTI, GTI_media, GTI_max, GTI_min, GTI_stddev, tensao_A, tensao_B, temperatura_A, temperatura_B)        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(dados[0][0],dados[1][0],dados[2][0],dados[3][0],dados[4][0],dados[5][0],dados[6][0], dados[7][0],dados[8][0],dados[9][0],dados[10][0],dados[11][0],dados[12][0],dados[13][0],dados[14][0],dados[15][0],dados[16][0],dados[17][0],dados[18][0],dados[19][0],dados[20][0],dados[21][0],dados[22][0],dados[23][0],dados[24][0],dados[25][0],dados[26][0],dados[27][0],dados[28][0],dados[29][0],dados[30][0],dados[31][0],dados[32][0],dados[33][0],dados[34][0],dados[35][0],dados[36][0],dados[37][0],dados[38][0],dados[39][0],dados[40][0],dados[41][0],dados[42][0],dados[43][0],dados[44][0],dados[45][0],dados[46][0],dados[47][0],dados[48][0],dados[49][0],dados[50][0],dados[51][0],dados[52][0],dados[53][0]))

    #fechar acesso
    conn.commit()
    print ('Base de dados ''ammonit'' atualizada')
    #c.close()
    #print ('Base de dados ''ammonit'' desconectada')


create_table()

# Loop infinito de update de base de dados
i=1
while True:
    # Atualiza banco de dados
    data_entry()
    print(i)
    # Tempo de amostragem
    time.sleep(1)
    if i == 10:
        break
    else:
        i+=1

c.close()
print ('Base de dados ''ammonit'' desconectada')

