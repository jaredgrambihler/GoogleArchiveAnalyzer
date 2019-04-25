import GoogleArchive
import time

def main():
    start = time.time()
    GoogleArchive.analyzeData()
    end = time.time()
    print('Finished in '+ str(end-start) + 's' )
    input('Press any key to exit.')

if __name__ == '__main__':
    main()
