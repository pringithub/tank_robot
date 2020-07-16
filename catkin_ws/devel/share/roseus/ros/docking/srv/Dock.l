;; Auto-generated. Do not edit!


(when (boundp 'docking::Dock)
  (if (not (find-package "DOCKING"))
    (make-package "DOCKING"))
  (shadow 'Dock (find-package "DOCKING")))
(unless (find-package "DOCKING::DOCK")
  (make-package "DOCKING::DOCK"))
(unless (find-package "DOCKING::DOCKREQUEST")
  (make-package "DOCKING::DOCKREQUEST"))
(unless (find-package "DOCKING::DOCKRESPONSE")
  (make-package "DOCKING::DOCKRESPONSE"))

(in-package "ROS")





(defclass docking::DockRequest
  :super ros::object
  :slots (_fiducial_id _waypoints ))

(defmethod docking::DockRequest
  (:init
   (&key
    ((:fiducial_id __fiducial_id) 0)
    ((:waypoints __waypoints) "")
    )
   (send-super :init)
   (setq _fiducial_id (round __fiducial_id))
   (setq _waypoints (string __waypoints))
   self)
  (:fiducial_id
   (&optional __fiducial_id)
   (if __fiducial_id (setq _fiducial_id __fiducial_id)) _fiducial_id)
  (:waypoints
   (&optional __waypoints)
   (if __waypoints (setq _waypoints __waypoints)) _waypoints)
  (:serialization-length
   ()
   (+
    ;; int32 _fiducial_id
    4
    ;; string _waypoints
    4 (length _waypoints)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _fiducial_id
       (write-long _fiducial_id s)
     ;; string _waypoints
       (write-long (length _waypoints) s) (princ _waypoints s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _fiducial_id
     (setq _fiducial_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _waypoints
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _waypoints (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass docking::DockResponse
  :super ros::object
  :slots (_success _message ))

(defmethod docking::DockResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional __success)
   (if __success (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass docking::Dock
  :super ros::object
  :slots ())

(setf (get docking::Dock :md5sum-) "112bdf241f064beb58699184e7082608")
(setf (get docking::Dock :datatype-) "docking/Dock")
(setf (get docking::Dock :request) docking::DockRequest)
(setf (get docking::Dock :response) docking::DockResponse)

(defmethod docking::DockRequest
  (:response () (instance docking::DockResponse :init)))

(setf (get docking::DockRequest :md5sum-) "112bdf241f064beb58699184e7082608")
(setf (get docking::DockRequest :datatype-) "docking/DockRequest")
(setf (get docking::DockRequest :definition-)
      "int32 fiducial_id
string waypoints
---
bool success
string message

")

(setf (get docking::DockResponse :md5sum-) "112bdf241f064beb58699184e7082608")
(setf (get docking::DockResponse :datatype-) "docking/DockResponse")
(setf (get docking::DockResponse :definition-)
      "int32 fiducial_id
string waypoints
---
bool success
string message

")



(provide :docking/Dock "112bdf241f064beb58699184e7082608")


