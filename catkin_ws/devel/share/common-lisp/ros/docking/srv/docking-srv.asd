
(cl:in-package :asdf)

(defsystem "docking-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Dock" :depends-on ("_package_Dock"))
    (:file "_package_Dock" :depends-on ("_package"))
  ))