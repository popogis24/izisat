        
from misc.connections import Connections
from misc.utils import Utils
from misc.files import Files
from loguru import logger

class IZISentinel:
    def __init__(self, output_base_path):
        """Initializes the Sentinel2_Band_Downloader instance."""
        self.output_base_path = output_base_path
               
        
    def connect_to_api(self, username, password):
        """Connects to the Sentinel API and obtains an access token."""
        connections = Connections()
        access_token, refresh_token, dt_access_token = connections.access_token(username, password)
        return access_token, refresh_token, dt_access_token
                                      
    def construct_query(self, footprint, start_date, end_date, cloud_cover_percentage, type, platform_name):
        """Constructs a query for retrieving Sentinel-2 products based on specified parameters."""
        utils = Utils()
        query = utils.construct_query_for_sentinel2_products(footprint, start_date, end_date, cloud_cover_percentage, type, platform_name)
        return query
        
    def products_from_sentinel_2(self, params):
        """Retrieves Sentinel-2 products based on the provided query parameters."""
        connections = Connections()
        products = connections.retrieve_sent_prod_from_query(params)
        return products
    
    def get_products_info(self, products):
        """Retrieves information about Sentinel-2 products."""
        utils = Utils()
        products_info = utils.retrieve_products_info(products)
        return products_info
    
    def output_folder(self, products_info, bands_dict):
        """Creates output folders to save downloaded bands."""
        files = Files()
        directory_paths = files.create_output_folders(self.output_base_path, products_info, bands_dict)
        return directory_paths
    
    def get_bands_links(self, access_token, products_info, bands_dict):
        """Retrieves links to bands for Sentinel-2 products."""
        connections = Connections()
        bands_links = connections.retrieve_bands_links(access_token, products_info, bands_dict)
        return bands_links
    
    def download_band(self, access_token, products_info, bands_link, base_dir, dt_access_token, refresh_token, tile):
        """Downloads bands for Sentinel-2 products based on the provided links."""
        connections = Connections()
        connections.download_bands(access_token, products_info, bands_link, base_dir, dt_access_token, refresh_token, tile)
        

    def download_sentinel2_bands(self, access_token, params, bands_dict, dt_access_token, refresh_token, tile):
        """Orchestrates the download process for Sentinel-2 bands."""
        products = self.products_from_sentinel_2(params)
        if products is None:
            logger.warning("Stopping further execution.")
        else:
            products_info = self.get_products_info(products)
            self.output_folder(products_info, bands_dict)
            links = self.get_bands_links(access_token, products_info, bands_dict)
            self.download_band(access_token, products_info, links, self.output_base_path, dt_access_token, refresh_token, tile)
            
            return products_info
        