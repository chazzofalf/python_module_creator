import sys
import python_module_creator
def main():
    if len(sys.argv) == 1:
        print_help()
    elif len(sys.argv) == 2:        
        python_module_creator(sys.argv[1])
    elif len(sys.argv) == 3:
        python_module_creator(sys.argv[1],sys.argv[2] == 'True')
    elif len(sys.argv) == 4:
        python_module_creator(sys.argv[1],sys.argv[2] == 'True',sys.argv[3] == 'True')
    
def print_help():
    print('python -m python_module_creator name:str dryrun:bool')
if __name__=="__main__":
    main()