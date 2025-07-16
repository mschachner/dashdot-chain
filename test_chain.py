import unittest
import chain

class TestRewriteStep(unittest.TestCase):
    def test_rule1(self):
        self.assertEqual(chain.rewrite_step('•0•3'), '•4')

    def test_rule2(self):
        self.assertEqual(chain.rewrite_step('-0•'), '•')

    def test_rule3(self):
        self.assertEqual(
            chain.rewrite_step('•0-0-3-5•2'),
            '•2-2-2-5•2'
        )

    def test_rule4(self):
        self.assertEqual(chain.rewrite_step('•3-5•2'), '•2-5•2-5•2')

if __name__ == '__main__':
    unittest.main()
