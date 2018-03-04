from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name='compare-mp3',

        version='0.1.0',

        description='Compare mp3 files using Python.',
        long_description='Compare mp3 files using Python.',

        url='https://github.com/mvasilkov/python-compare-mp3',

        author='Mark Vasilkov',
        author_email='mvasilkov@gmail.com',

        license='MIT',

        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Multimedia :: Sound/Audio',
        ],

        keywords='compare lame mp3',

        packages=find_packages(),
        include_package_data=True,

        install_requires=[
            'mutagen>=1.41.1',
        ],

        entry_points={
            'console_scripts': [
                'compare-mp3=compare_mp3:run',
            ],
        },
    )
