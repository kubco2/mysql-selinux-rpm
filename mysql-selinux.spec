# defining macros needed by SELinux
%global selinuxtype targeted
%global moduletype contrib
%global modulename mysql

Name: mysql-selinux
Version: 1.0.0
Release: 2%{?dist}
License: GPLv2
URL: https://github.com/kubco2/mysql-selinux
Summary: SELinux policies for product
Source0: mysql-selinux.tar.gz
BuildArch: noarch
BuildRequires: selinux-policy
%{?selinux_requires}

%description
SELinux policy modules for product.

%prep
%setup -q -n %{name}

%pre
%selinux_relabel_pre -s %{selinuxtype}

%build
make

%install
# install policy modules
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages

%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Wed Jul 18 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-1
- First Build

