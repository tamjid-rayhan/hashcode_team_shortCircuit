#Import section
import math
#Defined functions
def read_input():

    data = {}
    libraries = []
    library = {}
    fname = input("Enter file name = ")

    if(len(fname)<1):
        fname = 'a_example.txt'

    fhandle = open(fname)
    linecount = 0

    for line in fhandle:
        line = line.strip()
        nums = [int(num) for num in line.split()]

        if linecount ==0:
            data['counts']= {}
            data['counts']['books'] = nums[0]
            data['counts']['libraries'] = nums[1]
            data['counts']['days'] = nums[2]
            linecount += 1
            continue

        if linecount == 1:
            scores = dict()
            data['scores']= {}
            for i in range(len(nums)):
                scores[i] = nums[i]
            data['scores'] = scores
            linecount+= 1
            continue


        if linecount>1 and linecount%2 == 0:
            library['bookcount'] = nums[0]
            library['signup'] = nums[1]
            library['ship'] = nums[2]
            linecount+= 1
            continue


        if linecount>1 and linecount%2 == 1:
            library['bookids'] = nums
            print(library)
            libraries.append(library)
            linecount+= 1
            continue



    data['libraries'] = libraries
    return data

def read():
    fname = input("Enter file name = ")

    if(len(fname)<1):
        fname = 'a_example.txt'
    f = open(fname)

    # print(f.readline())
    f1 = f.readline().split()

    gg = dict()
    gg['counts'] = dict()
    gg['counts']['books'] = int(f1[0])
    gg['counts']['libraries'] = int(f1[1])
    gg['counts']['days'] = int(f1[2])

    #print(gg)
    # print(f.readline())
    f1 = f.readline().split()

    gg['scores'] = dict()
    for i in range(len(f1)):
        gg['scores'][i] = int(f1[i])

    #print(gg)
    gg['libraries'] = list()
    #print(gg)
    for i in range(gg['counts']['libraries']):
        #print(f.readline())
        f1 = f.readline().split()
        #print(f1)
        #print(i)
        d = dict()
        d['bookcount'] = int(f1[0])
        d['signup'] = int(f1[1])
        d['ship'] = int(f1[2])

        #print(f.readline())
        f1 = f.readline().split()
        d['bookids'] = [int(i) for i in f1]
        gg['libraries'].append(d)
        #print(gg)


    #print(gg)
    f.close()
    return gg

def write_output(libraries,data):
    fname = input("Enter file name = ")

    if(len(fname)<1):
        fname = 'a_example.out'
    f = open(fname,'w+')
    f.write(str(len(libraries)) + '\n')
    for library in libraries:
        library_id = str(library)
        #print(library_id)
        bookids = data['libraries'][library]['bookids']
        nobooks = str(len(bookids))
        #print(nobooks)
        first_line = library_id + ' ' + nobooks
        f.write(first_line + '\n')
        second_line = ''
        for book in bookids:
            second_line += str(book) + ' '
        f.write(second_line+'\n')
    return

def lib_score(gg):
    # per day score for each library.
    lib_score = dict()

    for i in range(gg['counts']['libraries']):

        num = 0
        bookids = gg['libraries'][i]['bookids']
        #print(gg['scores'])
        #print(bookids)
        # total score in the library
        for j in bookids:
            num += gg['scores'][j]

        #print('num', num)
        # total days taken to scan all the books in the library including signup days.
        den = gg['libraries'][i]['signup'] + math.ceil(gg['libraries'][i]['bookcount']/gg['libraries'][i]['ship'])
        #print('den', den)


        lib_score[i] = num/den
    print(lib_score)
    return lib_score




def lib_pref(lib_score):
    #library number to do signup process first will have higher lib_score.
    sorted_val = sorted(lib_score.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    #print(len(lib_score.values()))
    print()
    lib_pref = list()
    for i in range(len(lib_score.values())):
        #print(sorted_val[i][0])
        lib_pref.append(sorted_val[i][0])
    return lib_pref

#Main function
if __name__ == '__main__':
    #Read input data

    data = read()
    print(data)
    lib_score = lib_score(data)
    lib_pref= lib_pref(lib_score)
    write_output(lib_pref, data)
