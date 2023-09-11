x_axis = []
i = 0
x_min = 150
x_wid = 3500
res = 4096

step = x_wid/res
print(step)

for i in range(0,res):
    x_axis.append(i*step+x_min)

print(x_axis)
print(len(x_axis))