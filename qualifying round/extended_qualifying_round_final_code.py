import math
import time

def read(filename = 'a_example.txt'):
    """
      returns a dictionary of data read from the file
    """
    f = open(filename)
    f1 = f.readline().split()

    gg = dict()
    gg['counts'] = dict()
    gg['counts']['books'] = int(f1[0])
    gg['counts']['libraries'] = int(f1[1])
    gg['counts']['days'] = int(f1[2])

    f1 = f.readline().split()
    gg['scores'] = dict()
    for i in range(len(f1)):
        gg['scores'][i] = int(f1[i])

    gg['libraries'] = list()
    for i in range(gg['counts']['libraries']):
        f1 = f.readline().split()
        d = dict()
        d['bookcount'] = int(f1[0])
        d['signup'] = int(f1[1])
        d['ship'] = int(f1[2])

        f1 = f.readline().split()
        d['bookids'] = [int(i) for i in f1]
        gg['libraries'].append(d)

    f.close()
    return gg


def library_score(no_of_libraries, libraries, scores):
    # per day score for each library.
    
    #start_time = time.time()
    lib_score = dict()

    for i in range(no_of_libraries):
        num = 0
        total_scanable_books = 0
        bookids = libraries[i]['bookids']
        # total score in the library
        if len(bookids):
          for j in bookids:
              if scores[j]:
                total_scanable_books += 1
              num += scores[j]

          # total days taken to scan all the books in the library including signup days.
          den = libraries[i]['signup'] + math.ceil(total_scanable_books/libraries[i]['ship'])
          lib_score[i] = num/den
        else:
          lib_score[i] = 0
      #print(lib_score)
    #print("Library_score: %s seconds ---" % (time.time() - start_time))
    return lib_score
"""
def library_score(no_of_libraries, libraries, scores):
    # per day score for each library.
    
    #start_time = time.time()
    lib_score = dict()

    for i in range(no_of_libraries):
        num = 0
        bookids = libraries[i]['bookids']
        # total score in the library
        if len(bookids):
          for j in bookids:
              num += scores[j]

          # total days taken to scan all the books in the library including signup days.
          den = libraries[i]['signup'] + math.ceil(len(bookids)/libraries[i]['ship'])
          lib_score[i] = num/den
        else:
          lib_score[i] = 0
      #print(lib_score)
    #print("Library_score: %s seconds ---" % (time.time() - start_time))
    return lib_score
"""

def library_pref(lib_score):
    """
      Finds the library_id with highest score. 
      Returns the library_id and the score of that library 
    """
    #import time
    #start_time = time.time()
    #library number to do signup process first will have higher lib_score.
    sorted_val = sorted(lib_score.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    lib_pref = list()
    #print(sorted_val[0][0], sorted_val[0][1])
    
    # library_id
    lib_pref.append(sorted_val[0][0])
    # score of that library
    lib_pref.append(sorted_val[0][1])
    #print("Lib_pref: %s seconds ---" % (time.time() - start_time))
    return lib_pref

def uncommon(a, b):
    """
        returns uncommon values in a from b.
        a=[1,2,3,4,5]
        b=[1,2,3,7]
        >>uncommon(a,b)
        >>[4,5]
    """
    temp = list()
    for i in a:
        if i not in b:
            temp.append(i)
    return temp

def common(a,b):
    """
        returns common values in a and b.
        a=[1,2,3,4,5]
        b=[1,2,3,7]
        >>common(a,b)
        >>[1,2,3]
    """
    #start_time = time.time()
    c = [value for value in a if value in b]
    #print("common: %s seconds ---" % (time.time() - start_time))
    return c

def write_data(bookids, library_id, total, filename = 'a_example_out.txt'):
    
    
    f = open(filename,'a')

    nobooks = str(len(bookids))
    first_line = str(library_id) + ' ' + nobooks
    f.write(first_line + '\n')
    #print('firstline:', first_line)
    second_line = ''
    # the books that are not scanned yet from any library
    post_first = common(total, bookids)
    # the books that are already scanned or on the scanning process by some other library
    post_last = uncommon(bookids, post_first)
    for book in post_first:
        second_line += str(book) + ' '
    for book in post_last:
        second_line += str(book) + ' '
    #print('second_line', second_line)
    
    f.write(second_line+'\n')
    f.close()
    return




'''
file names:

b_read_on.txt
d_tough_choices.txt
e_so_many_books.txt
f_libraries_of_the_world.txt
c_incunabula.txt
'''

total_time = time.time()
read_filename = 'b_read_on.txt'
write_filename = 'b_read_on_out.txt'

data = read(read_filename)
#print(data)

# all the books i need to scan
total_books = [i for i in range(data['counts']['books'])]
total_libraries = data['counts']['libraries']
print('total Libraries:', total_libraries)

# will scan all the libraries in the data
f = open(write_filename,'w+')
f.write(str(data['counts']['libraries']) + '\n')
f.close()

# not used for any purposes
final_library_preferences = list()

# run total number or libraries times...
for i in range(total_libraries):
    
    # find a library with high score to scan
    lib_preference = library_pref(library_score(data['counts']['libraries'], data['libraries'], data['scores']))
    # at some point there will be only 0 score associated with the libraries. If that happes then we don't need to scan any more libraries
    # becaues they have no book that are not scanned.. but will have duplicate books at there disposal which we scanned already...
    if not lib_preference[1]:
      print('total libraries scanned: ', i+1)
      break;
    #print('lib_preference', lib_preference)
    library_id = lib_preference[0]
    final_library_preferences.append(library_id) # not used anywhere
    # print(library_id, end='')
    bookids = data['libraries'][library_id]['bookids']

    write_data(bookids, library_id, total_books, filename=write_filename)
    
    # update total_books list with not scanned books only
    total_books = uncommon(total_books, bookids)
    # make the score of the books we already scanned to zero.
    # this will help us calculate the best library with high score... because the books we sacnned will have no part in the calculation next time..
    for j in bookids:
      data['scores'][j] = 0
    data['libraries'][library_id]['bookids'] = []
    
    #print some crap to check the status...
    if (i+1) % 50 == 0:
      print('#', i+1, end=', ')
      if (i+1) % 1000 == 0:
        print('ReB:', len(total_books))

    if i == 3:
      print("One library write time: %s seconds" % ((time.time() - total_time)/ 4) )
      print("Estimated remaining time: %s seconds" % (total_libraries * ((time.time() - total_time)/4)))

# some libraries will have already scanned books in there bookids.. so we will find those libraries in the second phase
# write them to the file and make the calculation of total libraies scanned to total number of libraries... which we specified on write files first line!
# it was hard to change it afterwards and has some issues, so we will just do this again to make the equations equal... 

print('second phase...')
for library_id in range(total_libraries):
  # we dont need to check for score, because these will be the ones with zero score....
  bookids = data['libraries'][library_id]['bookids']
  # if some library has books in it, that means it wasn't scanned before... lets scan it now!
  if len(bookids):
    write_data(bookids, library_id, total_books, filename=write_filename)
    data['libraries'][library_id]['bookids'] = []
  
  if (library_id + 1) % 100 == 0:
    print('#', library_id+1, end=', ')
  if (library_id + 1) % 1000 == 0:
    print()

print("Total time: %s seconds." % (time.time() - total_time))
