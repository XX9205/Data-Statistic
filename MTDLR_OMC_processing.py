import re
import copy

def data_process():
    bw_data = [[0], [0], [0], [0], [0], [0]]       #len = 16
    time_interval = [3, 8, 6, 4, 7, 1, 8, 7]       # ordinary topo
    happen_time = [0]
    bw_sum = []
    data = {}
    data_traffic = {}
    for node in range(1, 8):
        happen_time.append(happen_time[node-1] + time_interval[node-1])
    print(happen_time)
    bw_ave = {}
    jitter_ave = {}
    loss_ave = {}
    traffic_load = [10, 20, 30]             #   10, 20, 30, 40, 50, 60, 70, 80, 90
    for load in traffic_load:
        avebw_list = []
        avejitter_list = []
        aveloss_list = []
        data_traffic[load] = []
        for file_num in range(1, 6):
            bw_sum = []
            avebw_sum = 0
            jitter_sum = 0
            loss_sum = 0
            bw_data = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
            throughtput = []
            for server_num in range(0, 6):
                file_object = open(r"C:\Users\dell\Desktop\一般拓扑测试数据\ECMP" + "\\" + str(load) + "\\" + str(file_num) + r"\server" + str(server_num) + '.txt')
                #   3-3-4   3-2-5   3-5-2  GLB(1-1)  GLB16
                try:
                    file_text = file_object.read()
                finally:
                    file_object.close()
                #print(file_text)
                pattern = re.compile('ytes\D\D(.*?)b', re.S)
                text_bw = re.findall(pattern, file_text)
                print(load, file_num, server_num)
                #print(text_bw)
                for i in range(0, len(text_bw)):
                    if text_bw[i].find("M") > 0:
                        text_bw[i] = float(text_bw[i][:-1])
                    elif text_bw[i].find("K") > 0:
                        text_bw[i] = float(text_bw[i][:-1]) / 1000
                    else:
                        text_bw[i] = float(text_bw[i]) / 1000000
                if text_bw:
                    avebw_sum = avebw_sum + text_bw[-1]
                    text_bw.pop()
                    bw_data[server_num] = text_bw
                else:
                    bw_data[server_num] = [0]

                jitter = re.compile('/sec\D\D(.*?)\Dms', re.S)
                text_jitter = re.findall(jitter, file_text)
                #print(text_jitter)
                for jitter in range(0, len(text_jitter)):
                    text_jitter[jitter] = float(text_jitter[jitter])
                if text_jitter:
                    jitter_sum = jitter_sum + text_jitter[-1]

                loss = re.compile('\D\((\d.*?)%', re.S)
                text_loss = re.findall(loss, file_text)
                print(text_loss)
                for loss in range(0, len(text_loss)):
                    text_loss[loss] = float(text_loss[loss])
                if text_loss:
                    loss_sum = loss_sum + text_loss[-1]
                    print(text_loss[-1])
                else:
                    loss_sum = loss_sum + 100

            avebw_list.append(float('%.5f' % (avebw_sum / 6)))
            avejitter_list.append(float('%.5f' % (jitter_sum / 6)))
            aveloss_list.append(float('%.5f' % (loss_sum / 6)))

            bw_sum = copy.deepcopy(bw_data[0])
            for text_num in range(1, 6):
                temp = copy.deepcopy(bw_data[text_num])
                for i in range(0, happen_time[text_num]):
                    temp.insert(0, 0)
                if len(temp) <= len(bw_sum):
                    for j in range(0, len(temp)):
                        bw_sum[j] = temp[j] + bw_sum[j]
                        bw_sum[j] = float('%.4f' % bw_sum[j])
                else:
                    for j in range(0, len(bw_sum)):
                        bw_sum[j] = temp[j] + bw_sum[j]
                        bw_sum[j] = float('%.4f' % bw_sum[j])
                    for j in range(len(bw_sum), len(temp)):
                        bw_sum.append(float('%.4f' % temp[j]))
            data[(load, file_num)] = bw_sum
            data_traffic[load].append(max(bw_sum))

        bw_ave[load] = avebw_list
        jitter_ave[load] = avejitter_list
        loss_ave[load] = aveloss_list

    data_text = open(r'C:\Users\dell\Desktop\一般拓扑测试数据\ECMP\data.txt', 'w')
    print(data, file=data_text)
    data_text.close()

    bw_ave_text = open(r'C:\Users\dell\Desktop\一般拓扑测试数据\ECMP\bw_ave.txt', 'w')
    print(bw_ave, file=bw_ave_text)
    bw_ave_text.close()

    jitter_ave_text = open(r'C:\Users\dell\Desktop\一般拓扑测试数据\ECMP\jitter_ave.txt', 'w')
    print(jitter_ave, file=jitter_ave_text)
    jitter_ave_text.close()

    loss_ave_text = open(r'C:\Users\dell\Desktop\一般拓扑测试数据\ECMP\loss_ave.txt', 'w')
    print(loss_ave, file=loss_ave_text)
    loss_ave_text.close()

    data_traffic_text = open(r'C:\Users\dell\Desktop\一般拓扑测试数据\ECMP\data_traffic.txt', 'w')
    print(data_traffic, file=data_traffic_text)
    data_traffic_text.close()

if __name__ == "__main__":
    data_process()