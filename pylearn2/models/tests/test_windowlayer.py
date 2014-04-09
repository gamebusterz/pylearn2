"""
Test for WindowLayer
"""
__authors__ = "Axel Davy"
__copyright__ = "Copyright 2014, Universite de Montreal"
__credits__ = ["Axel Davy"]
__license__ = "3-clause BSD"
__maintainer__ = "Axel Davy"

import numpy as np
import theano
from pylearn2.models.mlp import MLP, WindowLayer
from pylearn2.space import Conv2DSpace


def build_mlp_fn(x0, y0, x1, y1, s0, s1, c, axes):
    mlp = MLP(layers=[WindowLayer('h0', window=(x0, y0, x1, y1))],
              input_space=Conv2DSpace(shape=(s0, s1),
                                      num_channels=c, axes=axes))
    X = mlp.get_input_space().make_batch_theano()
    f = theano.function([X], mlp.fprop(X))
    return f

def test_windowlayer():
    np.testing.assert_raises(ValueError, build_mlp_fn,
                             0, 0, 20, 20, 20, 20, 3, ('c', 0, 1, 'b'))
    np.testing.assert_raises(ValueError, build_mlp_fn,
                             -1, -1, 19, 19, 20, 20, 3, ('c', 0, 1, 'b'))
    fprop = build_mlp_fn(5, 5, 10, 15, 20, 20, 2, ('b','c', 0, 1))
    n = np.random.rand(3, 2, 20, 20)
    r = fprop(n)
    assert r.shape == (3,2,6, 11)
    assert r[0, 0, 0, 0] == n[0, 0, 5, 5]
    assert r[2, 1, 5, 10] == n[2, 1, 10, 15]
    assert r[1, 1, 3, 3] == n[1, 1, 8, 8]

if __name__ == "__main__":
    test_windowlayer()

