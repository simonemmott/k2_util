from k2.settings import BASE_DIR, MAIN_DIR
import os
import logging
from k2.jinja2 import environment
from k2_app.models import Application
from jinja2 import PackageLoader

logger = logging.getLogger(__name__)

src_map = {
        'k2_domain/domain.name': {
            'name': '{{domain.name}}'
        },
        'k2_domain/domain.name/models/model.py': {
            'name': '[{% for model in domain.models.all() %}{{model.package_name()}}.py,{% endfor %}]',
            'keys': '[{% for model in domain.models.all() %}model={{model.id}},{% endfor %}]'
        }
    }
def _index_map(env, path, **kw):
    idx = {}
    name_template = env.from_string(src_map.get(path)['name'])
    name = name_template.render(**kw)
    if name[0] == '[':
        names = name[1:-2].split(',')
        keys_template = env.from_string(src_map.get(path)['keys'])
        keys = keys_template.render(**kw)[1:-2].split(',')
        for i in range(len(names)):
            idx[names[i]] = '{path}&{key}'.format(path=path, key=keys[i])
    else:
        idx[name] = '{path}'.format(path=path)
    return idx

def application_index(application: Application, **kw):
    idx = {}
    idx['.'] = 'k2_app'
    for app_domain in application.application_domains.all():
        idx[app_domain.domain.name] = '/k2_domain/src/{domain_id}?path=k2_domain/domain.name'.format(
            domain_id=app_domain.domain.id
        )
    return idx

def index(k2_domain, path, **kw):
    jinja2_env = environment(loader=PackageLoader(k2_domain, 'jinja2'))

    search_path = '/'.join([BASE_DIR, k2_domain, 'jinja2', path])
    if os.path.isdir(search_path):
        idx={}
        logger.debug('Indexing directory: {path}'.format(path=path))
        for file in os.listdir(search_path):
            f_path = '/'.join([path, file])
            if src_map.get(f_path):
                 idx.update(_index_map(jinja2_env, f_path, **kw))
            else:
                idx[file] = '{path}'.format(path=f_path)
        return idx
    else:
        raise ValueError("The path '{path} is not a directory".format(path=search_path))
    