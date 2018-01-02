# Copyright 2017 Xaptum, Inc.
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

import ecdaa

import ctypes

NONCE = 'nonce'

class PRNGException(Exception):
    pass

class CreationException(Exception):
    pass

class JoinException(Exception):
    pass

class SignException(Exception):
    pass

class VerifyException(Exception):
    pass

class SKRevFileException(Exception):
    pass

class Issuer(object):
    def __init__(self):
        self.prng = ecdaa.ecdaa_prng()
        ret = ecdaa.ecdaa_prng_init(ecdaa.pointer(self.prng))
        if 0 != ret:
            raise PRNGException('error initializing prng: ' + str(ret))

    def create_group(self):
        self.ipk = ecdaa.ecdaa_issuer_public_key_FP256BN()
        self.isk = ecdaa.ecdaa_issuer_secret_key_FP256BN()
        ret = ecdaa.ecdaa_issuer_key_pair_FP256BN_generate(ecdaa.pointer(self.ipk),
                                                           ecdaa.pointer(self.isk),
                                                           ecdaa.pointer(self.prng))
        if 0 != ret:
            raise CreationException('error creating issuer key-pair: ' + str(ret))

    def process_join_request(self, member_pk, nonce):
        cred = ecdaa.ecdaa_credential_FP256BN()
        cred_sig = ecdaa.ecdaa_credential_FP256BN_signature()
        ret = ecdaa.ecdaa_member_public_key_FP256BN_validate(ecdaa.pointer(member_pk),
                                                             nonce,
                                                             len(nonce))
        if 0 != ret:
            raise JoinException('member public key is invalid: ' + str(ret))

        ret = ecdaa.ecdaa_credential_FP256BN_generate(ecdaa.pointer(cred),
                                                      ecdaa.pointer(cred_sig),
                                                      ecdaa.pointer(self.isk),
                                                      ecdaa.pointer(member_pk),
                                                      ecdaa.pointer(self.prng))
        if 0 != ret:
            raise JoinException('error processing join request: ' + str(ret))

        return (cred, cred_sig)

class Member(object):
    def __init__(self, gpk):
        self.gpk = gpk

        self.prng = ecdaa.ecdaa_prng()
        ret = ecdaa.ecdaa_prng_init(ecdaa.pointer(self.prng))
        if 0 != ret:
            raise PRNGException('error initializing prng: ' + str(ret))

    def create_keypair(self, nonce):
        self.pk = ecdaa.ecdaa_member_public_key_FP256BN()
        self.sk = ecdaa.ecdaa_member_secret_key_FP256BN()
        ret = ecdaa.ecdaa_member_key_pair_FP256BN_generate(ecdaa.pointer(self.pk),
                                                           ecdaa.pointer(self.sk),
                                                           nonce,
                                                           len(nonce),
                                                           ecdaa.pointer(self.prng))
        if 0 != ret:
            raise JoinException('error creating join request: ' + str(ret))

    def process_join_response(self, cred, cred_sig):
        ret = ecdaa.ecdaa_credential_FP256BN_validate(ecdaa.pointer(cred),
                                                      ecdaa.pointer(cred_sig),
                                                      ecdaa.pointer(self.pk),
                                                      ecdaa.pointer(self.gpk))
        if 0 != ret:
            raise JoinException('credential signature is invalid: ' + str(ret))

        self.cred = cred

    def sign(self, message, basename):
        signature = ecdaa.ecdaa_signature_FP256BN()
        print('signing \'' + message + '\' of length ' + str(len(message)))
        ret = ecdaa.ecdaa_signature_FP256BN_sign(ecdaa.pointer(signature),
                                                 message,
                                                 len(message),
                                                 basename,
                                                 len(basename),
                                                 ecdaa.pointer(self.sk),
                                                 ecdaa.pointer(self.cred),
                                                 ecdaa.pointer(self.prng))
        if 0 != ret:
            raise SignException('error creating signature: ' + str(ret))

        return signature

def verify(gpk, message, signature, revocations, basename):
    print('verifying \'' + message + '\' of length ' + str(len(message)))
    ret = ecdaa.ecdaa_signature_FP256BN_verify(ecdaa.pointer(signature),
                                               ecdaa.pointer(gpk),
                                               ecdaa.pointer(revocations),
                                               message,
                                               len(message),
                                               basename,
                                               len(basename))

    return ret

def test_create_group():
    issuer = Issuer()
    issuer.create_group()

def test_create_member_keypair():
    issuer = Issuer()
    issuer.create_group()

    member = Member(issuer.ipk.gpk)
    member.create_keypair(NONCE)

def test_process_join_request():
    issuer = Issuer()
    issuer.create_group()

    member = Member(issuer.ipk.gpk)
    member.create_keypair(NONCE)

    cred,cred_sig = issuer.process_join_request(member.pk, NONCE)

def test_process_join_response():
    issuer = Issuer()
    issuer.create_group()

    member = Member(issuer.ipk.gpk)
    member.create_keypair(NONCE)

    cred,cred_sig = issuer.process_join_request(member.pk, NONCE)

    member.process_join_response(cred, cred_sig)

def test_sign_and_verify():
    issuer = Issuer()
    issuer.create_group()

    member = Member(issuer.ipk.gpk)
    member.create_keypair(NONCE)

    cred,cred_sig = issuer.process_join_request(member.pk, NONCE)

    member.process_join_response(cred, cred_sig)

    message = 'test message'
    signature = member.sign(message, 'BASENAME')

    revocations = ecdaa.ecdaa_revocations_FP256BN(sk_length=0, bsn_length=0)
    verify_ret = verify(issuer.ipk.gpk, message, signature, revocations, 'BASENAME')
    if (0 != verify_ret):
        raise VerifyException('signature NOT valid! ret = ' + str(verify_ret))

