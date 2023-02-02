import subprocess 

# Using system() method to
# execute shell commands
def process_file():
    result= str(subprocess.check_output('source ./process_files.sh',shell=True))
    resultArr=extract_validate_results(result)
    for line in resultArr:
        print(line)

def extract_validate_results(result ):
 # Clean up and format result
    result=result[2:-1]
    resultArr=result.split('\\r\\n')
    lastLine=resultArr[-1]
    resultArr=lastLine.split('\\n')
    print(f"resultArr size={len(resultArr)}\n")
    return resultArr
if __name__ == "__main__":
    process_file()