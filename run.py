import GoogleArchive
import time

def main():
    start = time.time()
    GoogleArchive.analyzeData(takeoutPath="Takeout/")
    end = time.time()
    print('Finished in {}s'.format(end-start))
    input('Press any key to exit.')

if __name__ == '__main__':
    main()
