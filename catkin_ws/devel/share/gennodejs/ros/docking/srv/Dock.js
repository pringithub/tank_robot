// Auto-generated. Do not edit!

// (in-package docking.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class DockRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.fiducial_id = null;
      this.waypoints = null;
    }
    else {
      if (initObj.hasOwnProperty('fiducial_id')) {
        this.fiducial_id = initObj.fiducial_id
      }
      else {
        this.fiducial_id = 0;
      }
      if (initObj.hasOwnProperty('waypoints')) {
        this.waypoints = initObj.waypoints
      }
      else {
        this.waypoints = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type DockRequest
    // Serialize message field [fiducial_id]
    bufferOffset = _serializer.int32(obj.fiducial_id, buffer, bufferOffset);
    // Serialize message field [waypoints]
    bufferOffset = _serializer.string(obj.waypoints, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type DockRequest
    let len;
    let data = new DockRequest(null);
    // Deserialize message field [fiducial_id]
    data.fiducial_id = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [waypoints]
    data.waypoints = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.waypoints.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'docking/DockRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '826f5b01681469068c9a8613e832ec93';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 fiducial_id
    string waypoints
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new DockRequest(null);
    if (msg.fiducial_id !== undefined) {
      resolved.fiducial_id = msg.fiducial_id;
    }
    else {
      resolved.fiducial_id = 0
    }

    if (msg.waypoints !== undefined) {
      resolved.waypoints = msg.waypoints;
    }
    else {
      resolved.waypoints = ''
    }

    return resolved;
    }
};

class DockResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
      this.message = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
      if (initObj.hasOwnProperty('message')) {
        this.message = initObj.message
      }
      else {
        this.message = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type DockResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [message]
    bufferOffset = _serializer.string(obj.message, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type DockResponse
    let len;
    let data = new DockResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [message]
    data.message = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.message.length;
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'docking/DockResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '937c9679a518e3a18d831e57125ea522';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    string message
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new DockResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    if (msg.message !== undefined) {
      resolved.message = msg.message;
    }
    else {
      resolved.message = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: DockRequest,
  Response: DockResponse,
  md5sum() { return '112bdf241f064beb58699184e7082608'; },
  datatype() { return 'docking/Dock'; }
};
