"""Independent mathematical checks for the public analytical heat demo."""
import math
import unittest

L = 1.0

def heat(x, t, alpha, amplitude):
    return amplitude * math.sin(math.pi * x / L) * math.exp(-alpha * math.pi**2 * t / L**2)

class HeatReferenceTests(unittest.TestCase):
    def test_boundary_conditions(self):
        for alpha in (0.01, 0.1, 0.3):
            for t in (0, 0.5, 5):
                self.assertAlmostEqual(heat(0, t, alpha, 1), 0, places=12)
                self.assertAlmostEqual(heat(L, t, alpha, 1), 0, places=12)

    def test_initial_condition(self):
        for x in (0.1, 0.25, 0.5, 0.9):
            self.assertAlmostEqual(heat(x, 0, 0.1, 2), 2*math.sin(math.pi*x), places=12)

    def test_pde_residual(self):
        dx, dt = 0.0005, 0.00001
        for alpha in (0.01, 0.1, 0.3):
            x, t = 0.4, 0.6
            ut = (heat(x,t+dt,alpha,1)-heat(x,t-dt,alpha,1))/(2*dt)
            uxx = (heat(x+dx,t,alpha,1)-2*heat(x,t,alpha,1)+heat(x-dx,t,alpha,1))/dx**2
            self.assertLess(abs(ut-alpha*uxx), 1e-6)

    def test_decay_and_linearity(self):
        self.assertGreater(heat(.5, .2, .1, 1), heat(.5, 1.0, .1, 1))
        self.assertAlmostEqual(heat(.5, 1, .1, 2), 2*heat(.5, 1, .1, 1), places=12)

if __name__ == "__main__":
    unittest.main()
