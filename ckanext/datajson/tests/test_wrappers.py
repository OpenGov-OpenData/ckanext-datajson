from ckanext.datajson.package2pod import Wrappers


class TestCatalogDateWrapper(object):

    def test_valid_dcat_issued_date(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "metadata_created": "2021-03-26T00:45:51.542432",
            "metadata_modified": "2021-03-26T00:45:51.542439",
            "extras": [
                {
                    "key": "dcat_issued",
                    "value": "2019-10-17T23:04:32.000Z"
                },
                {
                    "key": "dcat_modified",
                    "value": "2021-03-20T00:14:12.000Z"
                }
            ]
        }
        Wrappers.current_field_map = {
            "field": "metadata_created",
            "wrapper": "get_catalog_date"
        }
        issued_date = Wrappers.get_catalog_date(Wrappers.pkg.get('metadata_created'))
        assert issued_date == "2019-10-17T23:04:32.000Z"

    def test_valid_dcat_modified_date(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "metadata_created": "2021-03-26T00:45:51.542432",
            "metadata_modified": "2021-03-26T00:45:51.542439",
            "extras": [
                {
                    "key": "dcat_issued",
                    "value": "2019-10-17T23:04:32.000Z"
                },
                {
                    "key": "dcat_modified",
                    "value": "2021-03-20T00:14:12.000Z"
                }
            ]
        }
        Wrappers.current_field_map = {
            "field": "metadata_modified",
            "wrapper": "get_catalog_date"
        }
        modified_date = Wrappers.get_catalog_date(Wrappers.pkg.get('metadata_modified'))
        assert modified_date == "2021-03-20T00:14:12.000Z"

    def test_dcat_modified_only_field(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "metadata_created": "2021-03-26T00:45:51.542432",
            "metadata_modified": "2021-03-26T00:45:51.542439",
            "extras": [
                {
                    "key": "dcat_modified",
                    "value": "2021-03-20T00:14:12.000Z"
                }
            ]
        }
        Wrappers.current_field_map = {
            "field": "metadata_modified",
            "wrapper": "get_catalog_date"
        }
        modified_date = Wrappers.get_catalog_date(Wrappers.pkg.get('metadata_modified'))
        assert modified_date == "2021-03-26T00:45:51.542439"

    def test_no_dcat_in_extras(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "metadata_created": "2021-03-26T00:45:51.542432",
            "metadata_modified": "2021-03-26T00:45:51.542439",
            "extras": []
        }
        Wrappers.current_field_map = {
            "field": "metadata_modified",
            "wrapper": "get_catalog_date"
        }
        modified_date = Wrappers.get_catalog_date(Wrappers.pkg.get('metadata_modified'))
        assert modified_date == "2021-03-26T00:45:51.542439"


class TestGetLicenseWrapper(object):

    def test_valid_license_url(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "license_id": "cc-by",
            "license_title": "Creative Commons Attribution",
            "license_url": "http://www.opendefinition.org/licenses/cc-by"
        }
        Wrappers.current_field_map = {
            "field": "license_url",
            "wrapper": "get_license"
        }
        license = Wrappers.get_license(Wrappers.pkg.get('license_url'))
        assert license == "http://www.opendefinition.org/licenses/cc-by"

    def test_no_license_url(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "license_id": "other-open",
            "license_title": "Other (Open)"
        }
        Wrappers.current_field_map = {
            "field": "license_url",
            "wrapper": "get_license"
        }
        license = Wrappers.get_license(Wrappers.pkg.get('license_url'))
        assert license == "Other (Open)"

    def test_no_license_url_and_no_license_title(self):
        Wrappers.pkg = {
            "title": "Test Dataset",
            "name": "test-dataset",
            "license_id": None,
            "license_title": None
        }
        Wrappers.current_field_map = {
            "field": "license_url",
            "wrapper": "get_license"
        }
        license = Wrappers.get_license(Wrappers.pkg.get('license_url'))
        assert license is None
