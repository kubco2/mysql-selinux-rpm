# defining macros needed by SELinux
%global selinuxtype targeted
%global selinux_policyver 3.13.1-212
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
#Requires: selinux-policy >= %{selinux_policyver}
BuildRequires: git
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
#Requires(post): selinux-policy-base >= %{selinux_policyver}
#Requires(post): libselinux-utils
#Requires(post): policycoreutils
#%if 0%{?fedora}
#Requires(post): policycoreutils-python-utils
#%else
#Requires(post): policycoreutils-python
#%endif

%description
SELinux policy modules for product.

%prep
%setup -q -n %{name}

%build
make

%install
# install policy modules
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
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
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if

%changelog
* Wed Jul 18 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-1
- First Build

