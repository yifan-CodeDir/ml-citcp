import sys
import xml.etree.ElementTree as ET
import os
import csv
import pandas as pd
import understand
import time
import re

def xml_searching(path, test_class_name):
    
    for root, dirs, files in os.walk(path):
        #print(len(files))
        for x in files:
            #print(x)
            if x.endswith("." + test_class_name.replace("java","xml")):
                return(x)
    
def list_duplicates_remover(elems_duplicated_list):
    new_list = []
    for elem in elems_duplicated_list:
        if elem not in new_list:
            new_list.append(elem)
            
    return(new_list)

if __name__ == '__main__':
    #args[0] = execution time
    #args[1] = commit_id
    runtime = sys.argv[1]
    commit_id = sys.argv[2]          
    
    in_file = open("dependsby.txt","r")
    db_name = os.getcwd().split('/')[-1] + '.udb'
    db = understand.open("U_DB_DIR/" + db_name)
    # db = understand.open("U_DB_DIR/commons-math.udb")
    #out_file = open("testing_data.txt","a+")
    #out_file.write("test_class_name, tests, failures, time\n")
    

    duplicated_test_classes = in_file.read().split(",")  
    test_classes = list_duplicates_remover(duplicated_test_classes)
    #for i in range(0,len(test_classes)-1):
    #    print(test_classes[i])
    

    execution_data = pd.DataFrame()
    metrics_data = pd.DataFrame()
    pattern = re.compile('.*?(com.*?$)')
    for i in range(0,len(test_classes)-1):                    # for line in in_file:
        xml_name = xml_searching("target/surefire-reports", test_classes[i])        #xml_name = #TEST-org.apache.commons.math3.complex.ComplexFormatTest.xml
        #print(xlm_name)
        if xml_name:
            #parsing del file xml
            tree = ET.parse("target/surefire-reports/" + xml_name)  
            root = tree.getroot()
            #print(root.attrib.get('name'), root.attrib.get('tests'), root.attrib.get('failures'), root.attrib.get('time')) #time in secondi
            #out_file.write("%s, %s ,%s, %s\n" % (root.attrib.get('name'), root.attrib.get('tests'), root.attrib.get('failures'), root.attrib.get('time')))
            if float(root.attrib.get('tests')) <= 0.0:
                continue
            temp_data = pd.DataFrame({"test_class_name":[root.attrib.get('name').replace('.','/') + '.java'], "cycle_id":[commit_id],  "tests":[root.attrib.get('tests')], "failures":[root.attrib.get('failures')], "errors":[root.attrib.get('errors')], "failures_%":[float(root.attrib.get('failures')) / float(root.attrib.get('tests'))], "errors_%":[float(root.attrib.get('errors')) / float(root.attrib.get('tests'))], "time":[root.attrib.get('time')], "timestamp":[time.time()]})
            #execution_data = execution_data.append(temp_data, ignore_index = True)
            
            entity = db.lookup(xml_name.split('-')[-1].strip('.xml').replace('.','/') + '.java', "file") #cerco la classe nel database understand
            #print(xml_name.split('-')[-1].strip('.xml').replace('.','/') + '.java')    #org/apache/commons/math3/analysis/function/classTest.java
            for ent in entity:
                res = pattern.match(ent.longname())
                if res.group(1) == xml_name.split('-')[-1].strip('.xml').replace('.','/') + '.java':
                    ent_metrics = ent.metric(ent.metrics()) #metrics is a dictionary  (ent.metrics())
                    new_ent_metrics = {k: [v] for k, v in ent_metrics.items()}
                    temp_metrics_data = pd.DataFrame(new_ent_metrics)
                    temp_metrics_data.insert(0, 'test_class_name', res.group(1), allow_duplicates = True)
                    #print(temp_metrics_data)
                    metrics_data = metrics_data.append(temp_metrics_data, ignore_index = True) #provare a fare concat o join qui
                    temp_data = temp_data.join(temp_metrics_data.set_index('test_class_name'), on = 'test_class_name')
            
            execution_data = execution_data.append(temp_data, ignore_index = True)
        #else:
        #    print("NOTHING")

    cycle_data = pd.DataFrame({"cycle_id":[commit_id], "time_end_end[sec]":[runtime]})
    # execution_data = pd.concat([execution_data,metrics_data], axis = 'columns', join = 'inner', join_axes = [execution_data.index])
    # execution_data = execution_data.join(metrics_data.set_index('test_class_name'), on = 'test_class_name')
    #out_file.close()
    
    db.close()
    in_file.close()

    if not os.path.isfile('execution_data.csv'):
        execution_data.to_csv('execution_data.csv', index = False, header = True)
    else:
        execution_data.to_csv('execution_data.csv',index = False, mode = 'a', header = False) 
       

    if not os.path.isfile('cycle_data.csv'):
        cycle_data.to_csv('cycle_data.csv', index = False)
    else:
        cycle_data.to_csv('cycle_data.csv',index = False, mode = 'a', header=False)
    
    
    # if not os.path.isfile('metrics_data.csv'):
    #    metrics_data.to_csv('metrics_data.csv', index = False, header = True)
    # else:
    #    metrics_data.to_csv('metrics_data.csv',index = False, mode = 'a', header = False)

    mypath = "target/surefire-reports"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
    
