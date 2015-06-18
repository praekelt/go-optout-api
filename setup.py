from setuptools import setup, find_packages

setup(
    name="go-optouts",
    version="0.0.1a",
    url='http://github.com/praekelt/go-optouts-api',
    license='BSD',
    description="An API for managing Vumi Go opt outs.",
    long_description=open('README.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekeltfoundation.org',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'klein',
        'treq',
        'Twisted>=13.1.0',
        'vumi>=0.5.4',
        'vumi-go',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
