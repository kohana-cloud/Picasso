# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: query.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bquery.proto\x12\x04grpc\"\x07\n\x05\x45mpty\"3\n\tHoneypots\x12\x17\n\x0fHoneypotsAsJSON\x18\x01 \x01(\t\x12\r\n\x05\x63ount\x18\x02 \x01(\r\"#\n\x08Honeypot\x12\x17\n\x0fHoneypotsAsJSON\x18\x01 \x01(\t\"\x1d\n\rStartHoneypot\x12\x0c\n\x04type\x18\x01 \x01(\t\"\x1f\n\nReturnCode\x12\x11\n\terrorCode\x18\x01 \x01(\r\"&\n\x05\x45vent\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t2q\n\x0bQueryServer\x12,\n\x0cGetHoneypots\x12\x0b.grpc.Empty\x1a\x0f.grpc.Honeypots\x12\x34\n\x0bNewHoneypot\x12\x13.grpc.StartHoneypot\x1a\x10.grpc.ReturnCode2k\n\x18HoneypotManagementServer\x12(\n\nChatStream\x12\x0b.grpc.Empty\x1a\x0b.grpc.Event0\x01\x12%\n\tSendEvent\x12\x0b.grpc.Event\x1a\x0b.grpc.Emptyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_HONEYPOTS = DESCRIPTOR.message_types_by_name['Honeypots']
_HONEYPOT = DESCRIPTOR.message_types_by_name['Honeypot']
_STARTHONEYPOT = DESCRIPTOR.message_types_by_name['StartHoneypot']
_RETURNCODE = DESCRIPTOR.message_types_by_name['ReturnCode']
_EVENT = DESCRIPTOR.message_types_by_name['Event']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'query_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Empty)
  })
_sym_db.RegisterMessage(Empty)

Honeypots = _reflection.GeneratedProtocolMessageType('Honeypots', (_message.Message,), {
  'DESCRIPTOR' : _HONEYPOTS,
  '__module__' : 'query_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Honeypots)
  })
_sym_db.RegisterMessage(Honeypots)

Honeypot = _reflection.GeneratedProtocolMessageType('Honeypot', (_message.Message,), {
  'DESCRIPTOR' : _HONEYPOT,
  '__module__' : 'query_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Honeypot)
  })
_sym_db.RegisterMessage(Honeypot)

StartHoneypot = _reflection.GeneratedProtocolMessageType('StartHoneypot', (_message.Message,), {
  'DESCRIPTOR' : _STARTHONEYPOT,
  '__module__' : 'query_pb2'
  # @@protoc_insertion_point(class_scope:grpc.StartHoneypot)
  })
_sym_db.RegisterMessage(StartHoneypot)

ReturnCode = _reflection.GeneratedProtocolMessageType('ReturnCode', (_message.Message,), {
  'DESCRIPTOR' : _RETURNCODE,
  '__module__' : 'query_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ReturnCode)
  })
_sym_db.RegisterMessage(ReturnCode)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), {
  'DESCRIPTOR' : _EVENT,
  '__module__' : 'query_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Event)
  })
_sym_db.RegisterMessage(Event)

_QUERYSERVER = DESCRIPTOR.services_by_name['QueryServer']
_HONEYPOTMANAGEMENTSERVER = DESCRIPTOR.services_by_name['HoneypotManagementServer']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=21
  _EMPTY._serialized_end=28
  _HONEYPOTS._serialized_start=30
  _HONEYPOTS._serialized_end=81
  _HONEYPOT._serialized_start=83
  _HONEYPOT._serialized_end=118
  _STARTHONEYPOT._serialized_start=120
  _STARTHONEYPOT._serialized_end=149
  _RETURNCODE._serialized_start=151
  _RETURNCODE._serialized_end=182
  _EVENT._serialized_start=184
  _EVENT._serialized_end=222
  _QUERYSERVER._serialized_start=224
  _QUERYSERVER._serialized_end=337
  _HONEYPOTMANAGEMENTSERVER._serialized_start=339
  _HONEYPOTMANAGEMENTSERVER._serialized_end=446
# @@protoc_insertion_point(module_scope)
