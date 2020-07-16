; Auto-generated. Do not edit!


(cl:in-package docking-srv)


;//! \htmlinclude Dock-request.msg.html

(cl:defclass <Dock-request> (roslisp-msg-protocol:ros-message)
  ((fiducial_id
    :reader fiducial_id
    :initarg :fiducial_id
    :type cl:integer
    :initform 0)
   (waypoints
    :reader waypoints
    :initarg :waypoints
    :type cl:string
    :initform ""))
)

(cl:defclass Dock-request (<Dock-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Dock-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Dock-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name docking-srv:<Dock-request> is deprecated: use docking-srv:Dock-request instead.")))

(cl:ensure-generic-function 'fiducial_id-val :lambda-list '(m))
(cl:defmethod fiducial_id-val ((m <Dock-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader docking-srv:fiducial_id-val is deprecated.  Use docking-srv:fiducial_id instead.")
  (fiducial_id m))

(cl:ensure-generic-function 'waypoints-val :lambda-list '(m))
(cl:defmethod waypoints-val ((m <Dock-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader docking-srv:waypoints-val is deprecated.  Use docking-srv:waypoints instead.")
  (waypoints m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Dock-request>) ostream)
  "Serializes a message object of type '<Dock-request>"
  (cl:let* ((signed (cl:slot-value msg 'fiducial_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'waypoints))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'waypoints))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Dock-request>) istream)
  "Deserializes a message object of type '<Dock-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'fiducial_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'waypoints) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'waypoints) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Dock-request>)))
  "Returns string type for a service object of type '<Dock-request>"
  "docking/DockRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Dock-request)))
  "Returns string type for a service object of type 'Dock-request"
  "docking/DockRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Dock-request>)))
  "Returns md5sum for a message object of type '<Dock-request>"
  "112bdf241f064beb58699184e7082608")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Dock-request)))
  "Returns md5sum for a message object of type 'Dock-request"
  "112bdf241f064beb58699184e7082608")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Dock-request>)))
  "Returns full string definition for message of type '<Dock-request>"
  (cl:format cl:nil "int32 fiducial_id~%string waypoints~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Dock-request)))
  "Returns full string definition for message of type 'Dock-request"
  (cl:format cl:nil "int32 fiducial_id~%string waypoints~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Dock-request>))
  (cl:+ 0
     4
     4 (cl:length (cl:slot-value msg 'waypoints))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Dock-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Dock-request
    (cl:cons ':fiducial_id (fiducial_id msg))
    (cl:cons ':waypoints (waypoints msg))
))
;//! \htmlinclude Dock-response.msg.html

(cl:defclass <Dock-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass Dock-response (<Dock-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Dock-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Dock-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name docking-srv:<Dock-response> is deprecated: use docking-srv:Dock-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <Dock-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader docking-srv:success-val is deprecated.  Use docking-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <Dock-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader docking-srv:message-val is deprecated.  Use docking-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Dock-response>) ostream)
  "Serializes a message object of type '<Dock-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Dock-response>) istream)
  "Deserializes a message object of type '<Dock-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Dock-response>)))
  "Returns string type for a service object of type '<Dock-response>"
  "docking/DockResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Dock-response)))
  "Returns string type for a service object of type 'Dock-response"
  "docking/DockResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Dock-response>)))
  "Returns md5sum for a message object of type '<Dock-response>"
  "112bdf241f064beb58699184e7082608")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Dock-response)))
  "Returns md5sum for a message object of type 'Dock-response"
  "112bdf241f064beb58699184e7082608")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Dock-response>)))
  "Returns full string definition for message of type '<Dock-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Dock-response)))
  "Returns full string definition for message of type 'Dock-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Dock-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Dock-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Dock-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Dock)))
  'Dock-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Dock)))
  'Dock-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Dock)))
  "Returns string type for a service object of type '<Dock>"
  "docking/Dock")