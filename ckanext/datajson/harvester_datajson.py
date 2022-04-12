from __future__ import absolute_import

import requests
from future import standard_library
from requests.exceptions import InvalidURL, HTTPError, SSLError

standard_library.install_aliases()

from ckanext.datajson.harvester_base import DatasetHarvesterBase

from .parse_datajson import parse_datajson_entry


class DataJsonHarvester(DatasetHarvesterBase):
    """
    A Harvester for /data.json files.
    """

    HARVESTER_VERSION = "0.9al"  # increment to force an update even if nothing has changed

    def info(self):
        return {
            "name": "datajson",
            "title": "/data.json",
            "description": "Harvests remote /data.json files",
        }

    def load_remote_catalog(self, harvest_job):
        try:
            response = requests.get(harvest_job.source.url, headers={"User-agent": "Data.gov/2.0"})
            response.raise_for_status()
        except HTTPError as e:
            self._save_gather_error("HTTP Error getting json source: %s." % (e), harvest_job)
            return []
        except (InvalidURL, SSLError) as e:
            self._save_gather_error("URL Error getting json source: %s." % (e), harvest_job)
            return []
        try:
            datasets = response.json()
        except UnicodeDecodeError:
            # try different encode
            try:
                datasets = response.json(encoding="cp1252")
            except BaseException:
                datasets = response.json(encoding="iso-8859-1")

        # The first dataset should be for the data.json file itself. Check that
        # it is, and if so rewrite the dataset"s title because Socrata exports
        # these items all with the same generic name that is confusing when
        # harvesting a bunch from different sources. It should have an accessURL
        # but Socrata fills the URL of these in under webService.
        if (isinstance(datasets, list) and len(datasets) > 0  # NOQA W503 W504
                and (datasets[0].get("accessURL") == harvest_job.source.url or  # NOQA W503 W504
                    datasets[0].get("webService") == harvest_job.source.url)  # NOQA W503 W504
                and datasets[0].get("title") == "Project Open Data, /data.json file"):  # NOQA W503 W504
            datasets[0]["title"] = "%s Project Open Data data.json File" % harvest_job.source.title

        catalog_values = None
        if isinstance(datasets, dict):
            # this is a catalog, not dataset array as in schema 1.0.
            catalog_values = datasets.copy()
            datasets = catalog_values.pop("dataset", [])

        return datasets, catalog_values

    def set_dataset_info(self, pkg, dataset, dataset_defaults, schema_version):
        parse_datajson_entry(dataset, pkg, dataset_defaults, schema_version)
