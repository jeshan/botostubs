import main


def test_acm_python3():
    output = main.get_class_output('acm')

    assert """class ACM(BaseClient):
    class AddTagsToCertificateRequest(Mapping):
        pass

    class Tag(Mapping):
        pass

    class DeleteCertificateRequest(Mapping):
        pass

    class DescribeCertificateRequest(Mapping):
        pass

    class DescribeCertificateResponse(Mapping):
        pass

    class ExportCertificateRequest(Mapping):
        pass

    class ExportCertificateResponse(Mapping):
        pass

    class PassphraseBlob(object):
        pass

    class GetCertificateRequest(Mapping):
        pass

    class GetCertificateResponse(Mapping):
        pass

    class ImportCertificateRequest(Mapping):
        pass

    class ImportCertificateResponse(Mapping):
        pass

    class CertificateBodyBlob(object):
        pass

    class PrivateKeyBlob(object):
        pass

    class CertificateChainBlob(object):
        pass

    class ListCertificatesRequest(Mapping):
        pass

    class ListCertificatesResponse(Mapping):
        pass

    class CertificateStatus(object):
        pass

    class Filters(Mapping):
        pass

    class ListTagsForCertificateRequest(Mapping):
        pass

    class ListTagsForCertificateResponse(Mapping):
        pass

    class RemoveTagsFromCertificateRequest(Mapping):
        pass

    class RequestCertificateRequest(Mapping):
        pass

    class RequestCertificateResponse(Mapping):
        pass

    class DomainNameString(object):
        pass

    class DomainValidationOption(Mapping):
        pass

    class CertificateOptions(Mapping):
        pass

    class ResendValidationEmailRequest(Mapping):
        pass

    class UpdateCertificateOptionsRequest(Mapping):
        pass

    def add_tags_to_certificate(self, Tags: List[Tag], CertificateArn: str):
        pass

    def delete_certificate(self, CertificateArn: str):
        pass

    def describe_certificate(self, CertificateArn: str) -> DescribeCertificateResponse:
        pass

    def export_certificate(self, Passphrase: PassphraseBlob, CertificateArn: str) -> ExportCertificateResponse:
        pass

    def get_certificate(self, CertificateArn: str) -> GetCertificateResponse:
        pass

    def import_certificate(self, PrivateKey: PrivateKeyBlob, Certificate: CertificateBodyBlob, CertificateArn: str=None, CertificateChain: CertificateChainBlob=None) -> ImportCertificateResponse:
        pass

    def list_certificates(self, CertificateStatuses: List[CertificateStatus]=None, Includes: Filters=None, NextToken: str=None, MaxItems: int=None) -> ListCertificatesResponse:
        pass

    def list_tags_for_certificate(self, CertificateArn: str) -> ListTagsForCertificateResponse:
        pass

    def remove_tags_from_certificate(self, Tags: List[Tag], CertificateArn: str):
        pass

    def request_certificate(self, DomainName: str, ValidationMethod: str=None, SubjectAlternativeNames: List[DomainNameString]=None, IdempotencyToken: str=None, DomainValidationOptions: List[DomainValidationOption]=None, Options: CertificateOptions=None, CertificateAuthorityArn: str=None) -> RequestCertificateResponse:
        pass

    def resend_validation_email(self, ValidationDomain: str, Domain: str, CertificateArn: str):
        pass

    def update_certificate_options(self, Options: CertificateOptions, CertificateArn: str):
        pass

""" == output
