import understand
import sys
import os

def dependency_searching(entities, lookup, file, depth):
    not_test_array = []
    
    for ent in entities:
        if lookup in ent.name():
            file.write("%s," % ent)
            #file.write("%s\r\n" % ent)
        else:
            refs = ent.dependsby()
            #print(refs.keys())
            for key in refs.keys():
                if lookup in key.name():
                    print("IN - " + key.name())
                    file.write("%s," % key)
                    #file.write("%s\r\n" % key)       
                else:
                    #print("NOT IN - " + key.name())
                    not_test_array.append(key)
    
    if (not_test_array and depth > 0):
        depth = depth - 1
        dependency_searching(not_test_array, lookup, file, depth)


if __name__ == '__main__':
    
    #Open Database
    args = sys.argv[1]

    db_name = os.getcwd().split('/')[-1] + '.udb'
    db = understand.open("U_DB_DIR/"+db_name)

    file = open("dependsby.txt","a+")

    entity = db.lookup(args, "file")
    print(entity)

    dependency_searching(entity, "Test", file, 1)

    file.close()
    db.close()



