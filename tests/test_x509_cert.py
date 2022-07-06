import os
import unittest
import json
import jc.parsers.x509_cert

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-ca-cert.der'), 'rb') as f:
            self.x509_ca_cert = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-and-key.pem'), 'r', encoding='utf-8') as f:
            self.x509_cert_and_key_pem = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-letsencrypt.pem'), 'r', encoding='utf-8') as f:
            self.x509_letsencrypt = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-multi-cert.pem'), 'r', encoding='utf-8') as f:
            self.x509_multi_cert = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-ca-cert.json'), 'r', encoding='utf-8') as f:
            self.x509_ca_cert_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-and-key.json'), 'r', encoding='utf-8') as f:
            self.x509_cert_and_key_pem_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-letsencrypt.json'), 'r', encoding='utf-8') as f:
            self.x509_letsencrypt_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-multi-cert.json'), 'r', encoding='utf-8') as f:
            self.x509_multi_cert_json = json.loads(f.read())


    def test_x509_cert_nodata(self):
        """
        Test 'x509_cert' with no data
        """
        self.assertEqual(jc.parsers.x509_cert.parse('', quiet=True), [])

    def test_x509_ca_cert(self):
        """
        Test 'cat x509-ca-cert.der' (CA cert in DER format)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_ca_cert, quiet=True), self.x509_ca_cert_json)

    def test_x509_cert_and_key(self):
        """
        Test 'cat x509-cert-and-key.pem' (combo cert and key file in PEM format)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_and_key_pem, quiet=True), self.x509_cert_and_key_pem_json)

    def test_x509_letsencrypt(self):
        """
        Test 'cat x509-letsencrypt.pem' (letsencrypt cert in PEM format)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_letsencrypt, quiet=True), self.x509_letsencrypt_json)

    def test_x509_multi_cert(self):
        """
        Test 'cat x509-multi-cert.pem' (PEM file with multiple certificates)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_letsencrypt, quiet=True), self.x509_letsencrypt_json)


if __name__ == '__main__':
    unittest.main()
