import copy


class Matrix(object):
    """
    Represents a matrix with supports following operators:
    *: multiply a number or a matrix (if allowed)
    +: add with a matrix of same dimension
    ~: inverse of the matrix
    """

    def __init__(self, data=None, rows=None, cols=None, fill=0):
        """
        Matrix([[1,2,3],[2,3,4])         creates the specific 2x3 matrix
        Matrix(rows=3, cols=4, fill=1)   creates a 3x4 matrix with 1s

        :param list[list[float] data:
        :param int rows:
        :param int cols:
        :param float fill:
        """
        if data:
            # we'd better deep copy it
            self._data = copy.deepcopy(data)
        elif rows and cols:
            self._data = [[fill] * cols for _ in xrange(rows)]

    def clone(self):
        # don't worry, the new matrix won't change my data
        return Matrix(data=self._data)

    @property
    def rows(self):
        return len(self._data)

    @property
    def cols(self):
        if self._data:
            return len(self._data[0])
        return 0

    def __getitem__(self, key):
        """
        :param tuple[int] key:
        :rtype float
        """
        assert isinstance(key, tuple) and len(key) == 2
        return self._data[key[0]][key[1]]

    def __setitem__(self, key, value):
        """
        :param tuple[int] key:
        :param float value:
        """
        assert isinstance(key, tuple) and len(key) == 2
        self._data[key[0]][key[1]] = value

    def row(self, index):
        return Matrix(data=[self._data[index]])

    def col(self, index):
        return Matrix(data=[[row[index]] for row in self._data])

    def __mul__(self, m):
        """
        :param Matrix|float m:
        :rtype Matrix:
        """
        if isinstance(m, (int, float)):
            return m * self
        elif isinstance(m, Matrix):
            assert self.cols == m.rows
            p = Matrix(rows=self.rows, cols=m.cols)
            for r in xrange(self.rows):
                for c in xrange(m.cols):
                    for k in xrange(0, self.cols):
                        p[r, c] += self[r, k] * m[k, c]
            return p
        else:
            raise Exception('Could not multiply a matrix with: %s' % m)

    def __rmul__(self, n):
        """
        :param float n:
        :rtype Matrix:
        """
        assert isinstance(n, (int, float))
        p = Matrix(rows=self.rows, cols=self.cols)
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                p[r, c] = self[r, c] * n
        return p

    def __add__(self, m):
        """
        :param Matrix m:
        :rtype Matrix:
        """
        assert isinstance(m, Matrix)
        assert self.rows == m.rows and self.cols == m.cols

        s = Matrix(rows=self.rows, cols=m.cols)
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                s[r, c] = self[r, c] + m[r, c]
        return s

    def __invert__(self):
        raise NotImplementedError()

    def transpose(self):
        """
        :rtype: Matrix
        """
        t = Matrix(rows=self.cols, cols=self.rows)
        for r in xrange(self.cols):
            for c in xrange(self.rows):
                t[r, c] = self[c, r]
        return t

    def __str__(self):
        return '\n'.join([' '.join(['% 3s' % i for i in row]) for row in self._data])

if __name__ == '__main__':
    A = Matrix([[1, 2, 3],
                [2, 3, 4],
                [3, 4, 5],
                [3, 5, 7]
                ])

    B = Matrix([[0, 1, 0],
                [1, 0, 0],
                [0, 0, 1]])
    print A * B
