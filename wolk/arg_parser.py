from .constants import AWSRegion

def parse_aws_region(region_arg: str) -> AWSRegion:

    for region in AWSRegion:
        if region_arg == region.value[0]:
            return region

    raise ValueError(f'Invalid AWS region {region_arg}')