from conans import AutoToolsBuildEnvironment, ConanFile, tools


class OpensshConan(ConanFile):
    name = 'openssh'
    version = '8.2p1'
    license = 'BSD 3-Clause'
    author = 'bobrofon@gmail.com'
    url = 'https://github.com/bobrofon/conan-openssh'
    description = 'Portable OpenSSH'
    topics = ('c', 'security', 'login', 'file-sharing', 'cryptography',
              'keychain')
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False],
               'with_pie': [True, False],
               'with_4in6': [True, False],
               'with_privsep_path': 'ANY'}
    default_options = {'shared': False,
                       'with_pie': True,
                       'with_4in6': True,
                       'with_privsep_path': '/var/tmp/empty'}
    requires = 'zlib/1.2.11', 'openssl/1.0.2u'
    build_requires = 'autoconf/2.69', 'm4/1.4.18'

    src_repo_folder = 'openssh'

    autotools = None

    def configure(self):
        if self.options.shared == False:
            self.options['zlib'].shared = False
            self.options['openssl'].shared = False

    def source(self):
        git_tag = 'V_8_2_P1'

        git = tools.Git(folder=self.src_repo_folder)
        git.clone('https://github.com/openssh/openssh-portable.git', git_tag)

    def build(self):
        self.run('autoreconf {}'.format(self.src_repo_folder))
        self.autotools = AutoToolsBuildEnvironment(self)

        args = ['--with-privsep-path={}'.format(self.options.with_privsep_path)]

        if self.options.shared == False:
            self.autotools.link_flags.append('-static')
        if self.options.with_pie == True:
            args.append('--with-pie')
        if self.options.with_4in6 == True:
            args.append('--with-4in6')

        self.autotools.configure(configure_dir=self.src_repo_folder, args=args)
        self.autotools.make()

    def package(self):
        self.autotools.install()
