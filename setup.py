from setuptools import setup, find_packages

setup(
    name='django-geoposition',
    version=__import__('geoposition').__version__,
    description='Django model field that can hold a geoposition, and corresponding admin widget. A fork of django-geoposition.',
    author='Andras Gefferth',
    author_email='',
    url='http://github.com/philippbosch/django-geoposition',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'geoposition': [
            'locale/*/LC_MESSAGES/*',
            'templates/geoposition/widgets/*.html',
            'static/geoposition/*',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
