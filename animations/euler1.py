class SieveAnimation:
    def __init__(self, n, ax):
        self.n = n
        self.ax = ax
        self.frame = 0
        self.primes = [False] * n
        self.markers = []
        self.setup()
    
    def setup(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.n+1)
        self.ax.set_ylim(0, 2)
        self.ax.set_title('Sieve of Eratosthenes')
        # Initialize with proper sequences
        self.markers = [
            self.ax.plot([i+1], [0.5], 'bo', markersize=8)[0] 
            for i in range(self.n)
        ]
    
    def update(self):
        if self.frame >= self.n:
            return False
            
        num = self.frame + 1
        if num == 1:  # Skip number 1
            self.frame += 1
            return True
            
        if not self.primes[self.frame]:
            # Mark as prime
            self.primes[self.frame] = True
            # Proper multiple marking
            start = max(num * num, num * 2)
            for multiple in range(start, self.n+1, num):
                idx = multiple - 1
                if idx < len(self.primes):
                    self.primes[idx] = False  # Mark as non-prime
        
        # Update visualization with sequences
        for i, m in enumerate(self.markers):
            y_val = [1] if self.primes[i] else [0.5]
            m.set_data([i+1], y_val)  # Both x and y as sequences
        
        self.frame += 1
        return True