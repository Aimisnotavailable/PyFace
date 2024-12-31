class Smooth:
    
    def moving_average(self, data, window_size):
        if not data or window_size <= 0:
            return []

        moving_averages = []
        for i in range(len(data) - window_size + 1):
            window = data[i:i + window_size]
            window_average = sum(window) / window_size
            moving_averages.append(window_average)
        return moving_averages

