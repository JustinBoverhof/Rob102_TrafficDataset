from data_functions import squareImage, parse_Xml_DATA, parse_Json_data
import os
import re
import json

def process(origin_img_path, new_img_to_path, origin_anotations_path, new_labels_to_path, general_folder_path, Json = False, Verify = False):
    prexist_img_file_count = len([f for f in os.listdir(new_img_to_path) if (f.endswith('.PNG') or f.endswith('.jpg'))])
    prexist_labels_file_count = len([f for f in os.listdir(new_labels_to_path) if f.endswith('.json')])
    anotations_to_add = [f for f in os.listdir(origin_anotations_path) if (f.endswith('.xml') or f.endswith('.json'))]
    images_to_add = [f for f in os.listdir(origin_img_path) if (f.endswith('.png') or f.endswith('.jpg'))]

    if (prexist_labels_file_count != prexist_img_file_count):
        print("ERROR: Mismatch of prexisting label and image files. Exiting code")
        return -1
    c = prexist_img_file_count
    
    for x, ano_file in enumerate(anotations_to_add):
        if(all(vals in [maxi,141] for vals in final_count)):
            break
        # print(x)
        # print(ano_file)
        # print(c)
        if (Json):
            Class,Cords,originP, origin_IMG_ID =  parse_Json_data(origin_anotations_path+ano_file)
            originP += '.jpg'
            from_ = "Coco_2017"
        else:
            Class,Cords = parse_Xml_DATA(origin_anotations_path+ano_file)
            originP = images_to_add[x]
            origin_IMG_ID = str(originP)
            from_ = "road sign detection dataset"
        #print(Class)
        for j in range(0,len(Cords),4):
            cj = j//4
            if(Cords[j+2]-Cords[j] < 40 and Cords[j+3]-Cords[j+1] < 40):
                continue
            
            skip = True

            label_indx = 0;
            for t, ls in enumerate(raw_label_names):
                if ((Class[cj] in ls) == True and final_count[t] < maxi):
                    skip = False
                    break
                label_indx += 1
            
            if(skip):
                continue

            newP = new_img_to_path+str(c).rjust(4,"0")+".PNG"
            goodimg = squareImage(origin_img_path+originP,newP,Cords[j:(j+4)],Verify)
            if (goodimg == -1):
                continue
            label = str(label_indx)
            final_count[label_indx] += 1
       
            data = {
                "cat": label,
                "original_label" : Class[cj],
                'origin_img' : origin_IMG_ID,
                'origin_dataset' : from_
            }

            # Open a file object in write mode
            with open(new_labels_to_path + str(c).rjust(4,"0") + '.json', 'w') as file:
                # Write the dictionary to the file object as a JSON string
                json.dump(data, file)

            # Close the file object
            file.close()

            c += 1;
            if (c % 100 == 0):
                print("Every Hundred: ", final_count)

    with open(general_folder_path + "stats.txt", 'w') as file:
        for i in range(0, len(final_labels)):
            file.write((final_labels[i] +' {}\n').format(final_count[i]))
        # Close the file object
        file.close()

    with open(general_folder_path + "classes.txt", 'w') as file:
        for i in range(0, len(final_labels)):
            file.write((final_labels[i] +' {}\n').format(str(i)))
        # Close the file object
        file.close()

    print(final_labels)
    print(final_count)

path = "C:/Users/bover/Desktop/UROP/DataSets/"
originimg = path + "Road Sign Dataset 1/Images/"
originano = path + "Road Sign Dataset 1/annotations/"
newimg = path + "Final/Images/"
newlabels = path + "Final/Labels/"


raw_label_names = [["stop", "Stop_Sign", '13'], ["crosswalk"], ["trafficlight", '10'], ['14'],["3"],["2"]]#,["1"],["18"],["17"],["23"]]
final_labels = ["Stop", "Cross", "Light", "Meter","Car","Bike"]#,"Person","Dog","Cat", "Bear"]
final_count = [0,0,0,0,0,0]#,0,0,0,0]

statspath = path + "Final/stats.txt"

maxi = 1500

if os.path.isfile(statspath):
    with open(statspath, "r") as file:
            c = 0
            lines = file.readlines()
            for line in lines:
                match = re.search(r"\d+", line)
                if match:
                    number = int(match.group())
                    final_count[c] = number
                    c += 1
    file.close()



process(originimg,newimg,originano,newlabels,path + "Final/")

originimg = path + "coco 2017/train2017/"
originano = path + "coco 2017/my_annotations/"
process(originimg,newimg,originano,newlabels,path + "Final/", True,False)
