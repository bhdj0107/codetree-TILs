def sol():
    n, s = map(int, input().split())
    nums = list(map(int, input().split()))
    
    minLen = n + 12
    interval_sum = 0
    
    end = 0
    for start in range(n):
        while interval_sum < s and end < n:
            interval_sum += nums[end]
            end += 1
            if interval_sum >= s:
                minLen = min(minLen, end - start)
        interval_sum -= nums[start]
    return minLen
print(sol())