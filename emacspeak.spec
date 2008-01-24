#
# TODO:	- rm not needed *.el
#
Summary:	Emacspeak - speech output interface to Emacs
Summary(pl.UTF-8):	Emacspeak - mówiony interfejs wyjściowy dla Emacsa
Name:		emacspeak
Version:	24
Release:	1
License:	GPL v2
Group:		Applications/Sound
Source0:	http://emacspeak.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	3ff73f803dd2562018085cecdbdbef83
Patch0:		%{name}-debian.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-emacspeak.conf.patch
Patch3:		%{name}-emacspeak.sh.patch
Patch4:		%{name}-tclsh.patch
URL:		http://emacspeak.sorceforge.net/
BuildRequires:	emacs
BuildRequires:	emacs-gnus
BuildRequires:	lynx
BuildRequires:	perl-base
BuildRequires:	texinfo
Requires:	emacs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emacspeak is a speech output system that will allow someone who
cannot see to work directly on a UNIX system.  Emacspeak is built on
top of Emacs.  Once you start emacs with emacspeak loaded, you get
spoken feedback for everything you do.  Your mileage will vary
depending on how well you can use Emacs.  There is nothing that you
cannot do inside Emacs :-).  This package includes speech servers
written in Tcl to support the DECtalk Express and DECtalk MultiVoice
speech synthesizers.  For other synthesizers, look for separate
speech server packages such as emacspeak-ss and eflite.

%description -l pl.UTF-8
Emacspeak to system wyjścia mówionego pozwalający niewidomym pracować
bezpośrednio na systemie uniksowym. Emacspeak jest zbudowany w oparciu
o Emacsa. Po uruchomieniu Emacsa z wczytanym Emacspeakiem otrzymujemy
mówione potwierdzenie wszystkiego, co robimy. Korzyści zależą od tego,
na ile dobrze umiemy korzystać z Emacsa - nie ma niczego, czego by się
nie dało w nim zrobić :-). Ten pakiet zawiera serwery mowy napisane w
Tcl-u do obsługi syntezatorów mowy DECtalk Express i DECtalk
MultiVoice. Dla innych syntezatorów dostępne są oddzielne pakiety
serwerów mowy, takie jak emacspeak-ss czy eflite.

%prep
%setup -q -n %{name}-%{version}.0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__make} config
%{__make} -j1 emacspeak

cd info
%{__perl} -pi-orig -e 's/^\@c\$$Id/@c $$Id/;             
	s/^\@raggedright//;
	s/\@setfilename\./@setfilename ./' emacspeak.texi

%{__perl} -pi-orig -e 's/^\s\{8\}//' tts-server.texi
%{__perl} -pi-orig -e 's/^ @section/@section/' tts.texi

texi2html -monolithic emacspeak.texi
for x in emacspeak tts-server tts; do
	mv $x.texi-orig $x.texi
done
lynx -dump -nolist emacspeak.html > emacspeak.txt

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D debian/emacspeak.conf $RPM_BUILD_ROOT%{_sysconfdir}/emacspeak.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc README debian/DOC debian/README.Debian debian/*.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/emacspeak.conf
%attr(755,root,root) %{_bindir}/*
%{_emacs_lispdir}/emacspeak
%{_infodir}/emacspeak.info*
%{_mandir}/man1/*.1*
