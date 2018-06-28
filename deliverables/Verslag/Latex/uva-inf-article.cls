% LaTeX PAV klasse voor artikelen en generieke documenten
% Onderdeel van het LaTeX template pakket Practicum Academische Vaardigheden

% Voor readme en meest recente versie, zie
% https://gitlab-fnwi.uva.nl/informatica/LaTeX-template.git

% Geschreven door Robert van Wijk, Stephan van Schaik, Willem Vermeulen en
% Stephen Swatman.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{uva-inf-article}
\LoadClass[10pt]{article}

\RequirePackage{hyperref}
\RequirePackage{attachfile}
\RequirePackage{etoolbox}
\RequirePackage{xparse}
\RequirePackage{pgffor}
\RequirePackage{arrayjobx}
\RequirePackage{graphicx}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{translations}
\RequirePackage{lipsum}
\RequirePackage{ifthen}
\RequirePackage{wrapfig}
\RequirePackage{xstring}
\RequirePackage[a4paper, left=35mm, right=35mm, top=35mm, bottom=35mm]{geometry}
\RequirePackage[utf8]{inputenc}

\input{uva-inf-common}

%------------------------------------------------------------------------------
%	INSTELLINGEN
%------------------------------------------------------------------------------

\newcommand*{\includesource}{}

\DeclareOption{source}{
    \renewcommand*{\includesource}{\begin{flushright}\attachfile{\jobname.tex}\end{flushright}}
    \attachfilesetup{description=LaTeX code, icon=Tag, mimetype=application/x-tex}
}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions

\reversemarginpar

%------------------------------------------------------------------------------
%	HEADERS, FOOTERS EN SECTIONS
%------------------------------------------------------------------------------

\pagestyle{fancy}
\lhead{\includegraphics[width=5cm]{\GetTranslation{uva_logo}}}
\rhead{\footnotesize \textsc {\@assignmenttype\\ \@assignment}}
\lfoot
{
\footnotesize
\begin{minipage}{0.8\textwidth}
\foreach \index in {1, ..., \value{authorcount}} {%
    \getprefix{author\index}\ifthenelse{\equal{\index}{\value{authorcount}}}{}{,}
}
\end{minipage}
}
\cfoot{}
\rfoot{\small \textsc {\GetTranslation{page} \thepage\ \GetTranslation{of} \pageref{LastPage}}}
\renewcommand{\footrulewidth}{0.5pt}

\fancypagestyle{firststyle}
 {
  \includesource
  \fancyhf{}
   \renewcommand{\headrulewidth}{0pt}
   \rfoot{\small \textsc {\GetTranslation{page} \thepage\ \GetTranslation{of} \pageref{LastPage}}}
 }

\def\addlines#1{%
  \IfSubStr{#1}{ }{%
  	\saveexpandmode
  	\expandarg
    \StrSubstitute{#1}{ }{\noexpand\\}}{#1}}
    \restoreexpandmode

\newcommand{\sectionauthor}[2][]{
\section[#2]{#2\protect\marginpar{\normalfont\footnotesize #1}}
}

\newcommand{\subsectionauthor}[2][]{
\subsection[#2]{#2\protect\marginpar{\normalfont\footnotesize #1}}
}

%------------------------------------------------------------------------------
%	VOORPAGINA
%------------------------------------------------------------------------------

\renewcommand*{\maketitle}{%
\thispagestyle{firststyle}
\begin{center}
\includegraphics[width=7cm]{\GetTranslation{uva_logo}}
\\[1cm]
	\textsc{\Large \@assignment}\\[0.2cm]
		\rule{\linewidth}{0.5pt} \\[0.4cm]
			{ \huge \bfseries \@title}
		\rule{\linewidth}{0.5pt} \\[0.2cm]
	{\large \@date  \\[0.4cm]}

	\begin{minipage}{0.4\textwidth}
		\begin{flushleft}
			\emph{\ifnum\value{authorcount}>1\relax
                    \GetTranslation{students}%
                  \else
                    \GetTranslation{student}%
                  \fi:}\\
			\foreach \index in {1, ..., \value{authorcount}} {%
                {\getprefix{author\index}\\ {\small \getprefix{uva\index}\\[0.2cm]}}
            }
		\end{flushleft}
	\end{minipage}
~
	\begin{minipage}{0.4\textwidth}
		\begin{flushright}
			\ifdefempty{\@tutor}{}{
    			\emph{\GetTranslation{tutor}:} \\
    			\@tutor \\[0.2cm]
			}
			\ifdefempty{\@mentor}{}{
    			\emph{\GetTranslation{mentor}:} \\
    			\@mentor \\[0.2cm]
			}
			\ifdefempty{\@group}{}{
    			\emph{\GetTranslation{group}:} \\
    			\@group \\[0.2cm]
    		}
			\ifdefempty{\@docent}{}{
    			\emph{\GetTranslation{lecturer}:} \\
    			\@docent \\[0.2cm]
    		}
			\ifdefempty{\@course}{}{
    			\emph{\GetTranslation{course}:} \\
    			\@course \\[0.2cm]
    		}
			\ifdefempty{\@courseid}{}{
    			\emph{\GetTranslation{course_id}:} \\
    			\@courseid \\[0.2cm]
			}
		\end{flushright}
	\end{minipage}\\[1 cm]
\end{center}
}
