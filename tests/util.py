__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'
import os


def get_resource_path(resource):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', resource))
