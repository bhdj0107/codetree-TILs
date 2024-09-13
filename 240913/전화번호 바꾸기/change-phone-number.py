a = list(input().split('-'))
a[1], a[2] = a[2], a[1]
print('-'.join(a))