fname = input("Enter file name = ")

if(len(fname)<1):
    fname = 'a_example.in'

fhandle = open(fname)

linecount = 0
max_slices = None # The maximum number of slices allowed
num_pizza = None # Total number of pizzas available
slice_nos = dict() # A dictionary containing index of pizza as key and number of slices as value

#-----------Read the two lines of the file within this for loop---------------------
for line in fhandle:
    line = line.strip()
    nums = [int(num) for num in line.split()]

    #------------Handle the first line of input here-------------------------
    if (linecount==0):
        max_slices = nums[0]
        num_pizza = nums[1]
        linecount+= 1
        continue

    #-----------Handle the second line of input here
    index = 0
    for num in nums:
        slice_nos[index] = num
        index+= 1

#--------------Now that all the required values are extracted, print them-------------
#--------------Remove it later--------------------------------------------------------
print("Maxium number of slices:",max_slices )
print("Number of available pizzas:", num_pizza)
print("Slice number for each pizza \n", slice_nos)

#----------sort the slice_nos in the descending order of number of slices(values)-----------
sorted_slice_nos = sorted([(v,k) for (k,v) in slice_nos.items()],reverse = True)
#--------------------remove this print later----------------------------
print("Sorted slice number for each pizza \n", sorted_slice_nos)

sum = 0
pizza_bucket = list()
pizza_count = 0

for pizza in sorted_slice_nos:
    slices = pizza[0]
    pizza_no = pizza[1]
    sum += slices
    if sum < max_slices:
        pizza_bucket.append(pizza_no)
        pizza_count += 1
        continue
    sum = sum -slices


print("Output line 1:",pizza_count)
print("Output line 2:", sorted(pizza_bucket))

print("SCORE IS ", sum)
