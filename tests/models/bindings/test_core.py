"""Tests for core bindings models."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.bindings.core import (
    ChannelBindingsObject,
    MessageBindingsObject,
    OperationBindingsObject,
    ServerBindingsObject,
)
from asyncapi3.models.bindings.http import (
    HTTPMessageBindings,
    HTTPOperationBindings,
)
from asyncapi3.models.bindings.kafka import (
    KafkaChannelBindings,
    KafkaMessageBindings,
    KafkaOperationBindings,
    KafkaServerBindings,
)
from asyncapi3.models.bindings.mqtt import (
    MQTTMessageBindings,
    MQTTOperationBindings,
    MQTTServerBindings,
)
from asyncapi3.models.bindings.sqs import (
    SQSChannelBindings,
    SQSQueue,
)
from asyncapi3.models.schema import Schema


class TestServerBindingsObject:
    """Tests for ServerBindingsObject model."""

    def test_server_bindings_validation_multiple_protocols(self) -> None:
        """Test ServerBindingsObject model validation with multiple protocols."""
        yaml_data = """
        mqtt:
          clientId: guest
          cleanSession: true
          bindingVersion: 0.2.0
        kafka:
          schemaRegistryUrl: 'https://my-schema-registry.com'
          schemaRegistryVendor: confluent
          bindingVersion: 0.5.0
        """
        data = yaml.safe_load(yaml_data)
        server_bindings = ServerBindingsObject.model_validate(data)

        # Verify structure
        assert server_bindings.mqtt is not None
        assert server_bindings.kafka is not None
        assert server_bindings.http is None
        assert server_bindings.ws is None

        # Verify MQTT binding
        assert isinstance(server_bindings.mqtt, MQTTServerBindings)
        assert server_bindings.mqtt.client_id == "guest"
        assert server_bindings.mqtt.clean_session is True
        assert server_bindings.mqtt.binding_version == "0.2.0"

        # Verify Kafka binding
        assert isinstance(server_bindings.kafka, KafkaServerBindings)
        assert (
            server_bindings.kafka.schema_registry_url
            == "https://my-schema-registry.com"
        )
        assert server_bindings.kafka.schema_registry_vendor == "confluent"
        assert server_bindings.kafka.binding_version == "0.5.0"

    def test_server_bindings_validation_single_protocol(self) -> None:
        """Test ServerBindingsObject model validation with single protocol."""
        yaml_data = """
        mqtt:
          clientId: my-client
          cleanSession: false
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        server_bindings = ServerBindingsObject.model_validate(data)

        # Verify structure
        assert server_bindings.mqtt is not None
        assert server_bindings.kafka is None
        assert server_bindings.http is None
        assert server_bindings.ws is None

        # Verify MQTT binding
        assert isinstance(server_bindings.mqtt, MQTTServerBindings)
        assert server_bindings.mqtt.client_id == "my-client"
        assert server_bindings.mqtt.clean_session is False
        assert server_bindings.mqtt.binding_version == "0.2.0"

    def test_server_bindings_validation_empty(self) -> None:
        """Test ServerBindingsObject model validation with empty bindings."""
        server_bindings = ServerBindingsObject.model_validate({})

        # Verify all bindings are None
        assert server_bindings.mqtt is None
        assert server_bindings.kafka is None
        assert server_bindings.http is None
        assert server_bindings.ws is None
        assert server_bindings.amqp is None
        assert server_bindings.amqp1 is None

    def test_server_bindings_serialization_multiple_protocols(self) -> None:
        """Test ServerBindingsObject serialization with multiple protocols."""
        server_bindings = ServerBindingsObject(
            mqtt=MQTTServerBindings(client_id="guest", clean_session=True),
            kafka=KafkaServerBindings(
                schema_registry_url="https://my-schema-registry.com",
                schema_registry_vendor="confluent",
            ),
        )
        expected: dict = {
            "mqtt": {
                "clientId": "guest",
                "cleanSession": True,
                "bindingVersion": "0.2.0",
            },
            "kafka": {
                "schemaRegistryUrl": "https://my-schema-registry.com",
                "schemaRegistryVendor": "confluent",
                "bindingVersion": "0.5.0",
            },
        }
        assert server_bindings.model_dump() == expected

    def test_server_bindings_serialization_empty(self) -> None:
        """Test ServerBindingsObject serialization with empty bindings."""
        server_bindings = ServerBindingsObject()
        expected: dict = {}
        assert server_bindings.model_dump() == expected


class TestChannelBindingsObject:
    """Tests for ChannelBindingsObject model."""

    def test_channel_bindings_validation_multiple_protocols(self) -> None:
        """Test ChannelBindingsObject model validation with multiple protocols."""
        yaml_data = """
        kafka:
          topicConfiguration:
            cleanup.policy:
              - delete
              - compact
            retention.ms: 604800000
            retention.bytes: 1000000000
            delete.retention.ms: 86400000
            max.message.bytes: 1048588
          bindingVersion: 0.5.0
        """
        data = yaml.safe_load(yaml_data)
        channel_bindings = ChannelBindingsObject.model_validate(data)

        # Verify structure
        assert channel_bindings.kafka is not None
        assert channel_bindings.mqtt is None
        assert channel_bindings.http is None
        assert channel_bindings.ws is None

        # Verify Kafka binding
        assert isinstance(channel_bindings.kafka, KafkaChannelBindings)
        # Check topic configuration fields individually
        config = channel_bindings.kafka.topic_configuration
        assert config.cleanup_policy == ["delete", "compact"]
        assert config.retention_ms == 604800000
        assert config.retention_bytes == 1000000000
        assert config.delete_retention_ms == 86400000
        assert config.max_message_bytes == 1048588
        assert channel_bindings.kafka.binding_version == "0.5.0"

    def test_channel_bindings_validation_single_protocol(self) -> None:
        """Test ChannelBindingsObject model validation with single protocol."""
        yaml_data = """
        kafka:
          topic: my-topic
          partitions: 3
          replicas: 2
          bindingVersion: 0.5.0
        """
        data = yaml.safe_load(yaml_data)
        channel_bindings = ChannelBindingsObject.model_validate(data)

        # Verify structure
        assert channel_bindings.kafka is not None
        assert channel_bindings.mqtt is None
        assert channel_bindings.http is None
        assert channel_bindings.ws is None

        # Verify Kafka binding
        assert isinstance(channel_bindings.kafka, KafkaChannelBindings)
        assert channel_bindings.kafka.topic == "my-topic"
        assert channel_bindings.kafka.partitions == 3
        assert channel_bindings.kafka.replicas == 2
        assert channel_bindings.kafka.binding_version == "0.5.0"

    def test_channel_bindings_validation_empty(self) -> None:
        """Test ChannelBindingsObject model validation with empty bindings."""
        channel_bindings = ChannelBindingsObject.model_validate({})

        # Verify all bindings are None
        assert channel_bindings.kafka is None
        assert channel_bindings.mqtt is None
        assert channel_bindings.http is None
        assert channel_bindings.ws is None
        assert channel_bindings.amqp is None
        assert channel_bindings.amqp1 is None

    def test_channel_bindings_serialization_multiple_protocols(self) -> None:
        """Test ChannelBindingsObject serialization with multiple protocols."""
        channel_bindings = ChannelBindingsObject(
            kafka=KafkaChannelBindings(
                topic_configuration={
                    "cleanup.policy": ["delete", "compact"],
                    "retention.ms": 604800000,
                    "retention.bytes": 1000000000,
                    "delete.retention.ms": 86400000,
                    "max.message.bytes": 1048588,
                }
            ),
            sqs=SQSChannelBindings(queue=SQSQueue(name="my-queue", fifo_queue=True)),
        )
        expected: dict = {
            "kafka": {
                "topicConfiguration": {
                    "cleanup.policy": ["delete", "compact"],
                    "retention.ms": 604800000,
                    "retention.bytes": 1000000000,
                    "delete.retention.ms": 86400000,
                    "max.message.bytes": 1048588,
                },
                "bindingVersion": "0.5.0",
            },
            "sqs": {
                "queue": {"name": "my-queue", "fifoQueue": True},
                "bindingVersion": "0.3.0",
            },
        }
        assert channel_bindings.model_dump() == expected

    def test_channel_bindings_serialization_empty(self) -> None:
        """Test ChannelBindingsObject serialization with empty bindings."""
        channel_bindings = ChannelBindingsObject()
        expected: dict = {}
        assert channel_bindings.model_dump() == expected


class TestOperationBindingsObject:
    """Tests for OperationBindingsObject model."""

    def test_operation_bindings_validation_multiple_protocols(self) -> None:
        """Test OperationBindingsObject model validation with multiple protocols."""
        yaml_data = """
        kafka:
          groupId:
            type: string
            enum:
              - my-app-id
          clientId:
            type: string
            enum:
              - my-client-id
          bindingVersion: 0.5.0
        mqtt:
          qos: 1
          retain: false
          bindingVersion: 0.2.0
        http:
          method: POST
          query:
            type: object
            properties:
              streetlightId:
                type: string
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        operation_bindings = OperationBindingsObject.model_validate(data)

        # Verify structure
        assert operation_bindings.kafka is not None
        assert operation_bindings.mqtt is not None
        assert operation_bindings.http is not None
        assert operation_bindings.ws is None

        # Verify Kafka binding
        assert isinstance(operation_bindings.kafka, KafkaOperationBindings)
        assert operation_bindings.kafka.group_id == Schema(
            type="string", enum=["my-app-id"]
        )
        assert operation_bindings.kafka.client_id == Schema(
            type="string", enum=["my-client-id"]
        )
        assert operation_bindings.kafka.binding_version == "0.5.0"

        # Verify MQTT binding
        assert isinstance(operation_bindings.mqtt, MQTTOperationBindings)
        assert operation_bindings.mqtt.qos == 1
        assert operation_bindings.mqtt.retain is False
        assert operation_bindings.mqtt.binding_version == "0.2.0"

        # Verify HTTP binding
        assert isinstance(operation_bindings.http, HTTPOperationBindings)
        assert operation_bindings.http.method == "POST"
        # Query is parsed as dict from YAML, check its structure
        assert operation_bindings.http.query.type == "object"
        assert "streetlightId" in operation_bindings.http.query.properties
        streetlight_prop = operation_bindings.http.query.properties["streetlightId"]
        assert streetlight_prop["type"] == "string"
        assert operation_bindings.http.binding_version == "0.3.0"

    def test_operation_bindings_validation_single_protocol(self) -> None:
        """Test OperationBindingsObject model validation with single protocol."""
        yaml_data = """
        mqtt:
          qos: 2
          retain: true
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        operation_bindings = OperationBindingsObject.model_validate(data)

        # Verify structure
        assert operation_bindings.mqtt is not None
        assert operation_bindings.kafka is None
        assert operation_bindings.http is None
        assert operation_bindings.ws is None

        # Verify MQTT binding
        assert isinstance(operation_bindings.mqtt, MQTTOperationBindings)
        assert operation_bindings.mqtt.qos == 2
        assert operation_bindings.mqtt.retain is True
        assert operation_bindings.mqtt.binding_version == "0.2.0"

    def test_operation_bindings_validation_empty(self) -> None:
        """Test OperationBindingsObject model validation with empty bindings."""
        operation_bindings = OperationBindingsObject.model_validate({})

        # Verify all bindings are None
        assert operation_bindings.kafka is None
        assert operation_bindings.mqtt is None
        assert operation_bindings.http is None
        assert operation_bindings.ws is None
        assert operation_bindings.amqp is None
        assert operation_bindings.amqp1 is None

    def test_operation_bindings_serialization_multiple_protocols(self) -> None:
        """Test OperationBindingsObject serialization with multiple protocols."""
        operation_bindings = OperationBindingsObject(
            kafka=KafkaOperationBindings(
                group_id=Schema(type="string", enum=["my-app-id"]),
                client_id=Schema(type="string", enum=["my-client-id"]),
            ),
            mqtt=MQTTOperationBindings(qos=1, retain=False),
            http=HTTPOperationBindings(
                method="POST",
                query=Schema(
                    type="object", properties={"streetlightId": Schema(type="string")}
                ),
            ),
        )
        expected: dict = {
            "kafka": {
                "groupId": {"type": "string", "enum": ["my-app-id"]},
                "clientId": {"type": "string", "enum": ["my-client-id"]},
                "bindingVersion": "0.5.0",
            },
            "mqtt": {"qos": 1, "retain": False, "bindingVersion": "0.2.0"},
            "http": {
                "method": "POST",
                "query": {
                    "type": "object",
                    "properties": {"streetlightId": {"type": "string"}},
                },
                "bindingVersion": "0.3.0",
            },
        }
        assert operation_bindings.model_dump() == expected

    def test_operation_bindings_serialization_empty(self) -> None:
        """Test OperationBindingsObject serialization with empty bindings."""
        operation_bindings = OperationBindingsObject()
        expected: dict = {}
        assert operation_bindings.model_dump() == expected


class TestMessageBindingsObject:
    """Tests for MessageBindingsObject model."""

    def test_message_bindings_validation_multiple_protocols(self) -> None:
        """Test MessageBindingsObject model validation with multiple protocols."""
        yaml_data = """
        kafka:
          key:
            type: string
            enum:
              - my-key
          bindingVersion: 0.5.0
        mqtt:
          payloadFormatIndicator: 1
          contentType: application/json
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        message_bindings = MessageBindingsObject.model_validate(data)

        # Verify structure
        assert message_bindings.kafka is not None
        assert message_bindings.mqtt is not None
        assert message_bindings.http is None
        assert message_bindings.ws is None

        # Verify Kafka binding
        assert isinstance(message_bindings.kafka, KafkaMessageBindings)
        assert message_bindings.kafka.key == Schema(type="string", enum=["my-key"])
        assert message_bindings.kafka.binding_version == "0.5.0"

        # Verify MQTT binding
        assert isinstance(message_bindings.mqtt, MQTTMessageBindings)
        assert message_bindings.mqtt.payload_format_indicator == 1
        assert message_bindings.mqtt.content_type == "application/json"
        assert message_bindings.mqtt.binding_version == "0.2.0"

    def test_message_bindings_validation_single_protocol(self) -> None:
        """Test MessageBindingsObject model validation with single protocol."""
        yaml_data = """
        http:
          headers:
            type: object
            properties:
              Content-Type:
                type: string
                enum:
                  - application/json
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        message_bindings = MessageBindingsObject.model_validate(data)

        # Verify structure
        assert message_bindings.http is not None
        assert message_bindings.kafka is None
        assert message_bindings.mqtt is None
        assert message_bindings.ws is None

        # Verify HTTP binding
        assert isinstance(message_bindings.http, HTTPMessageBindings)
        # Headers is parsed as dict from YAML, check its structure
        assert message_bindings.http.headers.type == "object"
        assert "Content-Type" in message_bindings.http.headers.properties
        content_type_prop = message_bindings.http.headers.properties["Content-Type"]
        assert content_type_prop["type"] == "string"
        assert content_type_prop["enum"] == ["application/json"]
        assert message_bindings.http.binding_version == "0.3.0"

    def test_message_bindings_validation_empty(self) -> None:
        """Test MessageBindingsObject model validation with empty bindings."""
        message_bindings = MessageBindingsObject.model_validate({})

        # Verify all bindings are None
        assert message_bindings.kafka is None
        assert message_bindings.mqtt is None
        assert message_bindings.http is None
        assert message_bindings.ws is None
        assert message_bindings.amqp is None
        assert message_bindings.amqp1 is None

    def test_message_bindings_serialization_multiple_protocols(self) -> None:
        """Test MessageBindingsObject serialization with multiple protocols."""
        message_bindings = MessageBindingsObject(
            kafka=KafkaMessageBindings(key=Schema(type="string", enum=["my-key"])),
            mqtt=MQTTMessageBindings(
                payload_format_indicator=1, content_type="application/json"
            ),
            http=HTTPMessageBindings(
                headers=Schema(
                    type="object",
                    properties={
                        "Content-Type": Schema(type="string", enum=["application/json"])
                    },
                )
            ),
        )
        expected: dict = {
            "kafka": {
                "key": {"type": "string", "enum": ["my-key"]},
                "bindingVersion": "0.5.0",
            },
            "mqtt": {
                "payloadFormatIndicator": 1,
                "contentType": "application/json",
                "bindingVersion": "0.2.0",
            },
            "http": {
                "headers": {
                    "type": "object",
                    "properties": {
                        "Content-Type": {"type": "string", "enum": ["application/json"]}
                    },
                },
                "bindingVersion": "0.3.0",
            },
        }
        assert message_bindings.model_dump() == expected

    def test_message_bindings_serialization_empty(self) -> None:
        """Test MessageBindingsObject serialization with empty bindings."""
        message_bindings = MessageBindingsObject()
        expected: dict = {}
        assert message_bindings.model_dump() == expected


class TestBindingsExtensions:
    """Tests for bindings objects extensions support."""

    def test_server_bindings_inherit_from_extendable_base_model(self) -> None:
        """Test that ServerBindingsObject inherits from ExtendableBaseModel."""
        from asyncapi3.models.base_models import ExtendableBaseModel

        # Check inheritance
        assert issubclass(ServerBindingsObject, ExtendableBaseModel)
        assert isinstance(ServerBindingsObject(), ExtendableBaseModel)

    def test_channel_bindings_inherit_from_extendable_base_model(self) -> None:
        """Test that ChannelBindingsObject inherits from ExtendableBaseModel."""
        from asyncapi3.models.base_models import ExtendableBaseModel

        # Check inheritance
        assert issubclass(ChannelBindingsObject, ExtendableBaseModel)
        assert isinstance(ChannelBindingsObject(), ExtendableBaseModel)

    def test_operation_bindings_inherit_from_extendable_base_model(self) -> None:
        """Test that OperationBindingsObject inherits from ExtendableBaseModel."""
        from asyncapi3.models.base_models import ExtendableBaseModel

        # Check inheritance
        assert issubclass(OperationBindingsObject, ExtendableBaseModel)
        assert isinstance(OperationBindingsObject(), ExtendableBaseModel)

    def test_message_bindings_inherit_from_extendable_base_model(self) -> None:
        """Test that MessageBindingsObject inherits from ExtendableBaseModel."""
        from asyncapi3.models.base_models import ExtendableBaseModel

        # Check inheritance
        assert issubclass(MessageBindingsObject, ExtendableBaseModel)
        assert isinstance(MessageBindingsObject(), ExtendableBaseModel)

    def test_server_bindings_valid_extensions(self) -> None:
        """Test ServerBindingsObject with valid x- extensions."""
        yaml_data = """
        mqtt:
          clientId: test
          bindingVersion: 0.2.0
        x-custom-extension: "custom value"
        x-vendor-specific: 123
        x-detailed.info: true
        """
        data = yaml.safe_load(yaml_data)
        server_bindings = ServerBindingsObject.model_validate(data)

        # Check that extensions are stored
        assert server_bindings.model_extra is not None
        assert server_bindings.model_extra["x-custom-extension"] == "custom value"
        assert server_bindings.model_extra["x-vendor-specific"] == 123
        assert server_bindings.model_extra["x-detailed.info"] is True

        # Check serialization includes extensions
        dumped = server_bindings.model_dump()
        assert "x-custom-extension" in dumped
        assert "x-vendor-specific" in dumped
        assert "x-detailed.info" in dumped

    def test_channel_bindings_valid_extensions(self) -> None:
        """Test ChannelBindingsObject with valid x- extensions."""
        yaml_data = """
        kafka:
          topic: my-topic
          bindingVersion: 0.5.0
        x-workflow-id: "wf-123"
        x-metadata: {"key": "value"}
        """
        data = yaml.safe_load(yaml_data)
        channel_bindings = ChannelBindingsObject.model_validate(data)

        # Check extensions
        assert channel_bindings.model_extra is not None
        assert channel_bindings.model_extra["x-workflow-id"] == "wf-123"
        assert channel_bindings.model_extra["x-metadata"] == {"key": "value"}

    def test_operation_bindings_valid_extensions(self) -> None:
        """Test OperationBindingsObject with valid x- extensions."""
        yaml_data = """
        http:
          method: GET
          bindingVersion: 0.3.0
        x-rate-limit: 100
        x-cache-ttl: 3600
        """
        data = yaml.safe_load(yaml_data)
        operation_bindings = OperationBindingsObject.model_validate(data)

        # Check extensions
        assert operation_bindings.model_extra is not None
        assert operation_bindings.model_extra["x-rate-limit"] == 100
        assert operation_bindings.model_extra["x-cache-ttl"] == 3600

    def test_message_bindings_valid_extensions(self) -> None:
        """Test MessageBindingsObject with valid x- extensions."""
        yaml_data = """
        http:
          headers:
            type: object
            properties:
              Content-Type:
                type: string
          bindingVersion: 0.3.0
        x-message-type: "event"
        x-schema-version: "1.2.3"
        """
        data = yaml.safe_load(yaml_data)
        message_bindings = MessageBindingsObject.model_validate(data)

        # Check extensions
        assert message_bindings.model_extra is not None
        assert message_bindings.model_extra["x-message-type"] == "event"
        assert message_bindings.model_extra["x-schema-version"] == "1.2.3"

    def test_server_bindings_invalid_extensions(self) -> None:
        """Test ServerBindingsObject with invalid extensions."""

        yaml_data = """
        mqtt:
          clientId: test
          bindingVersion: 0.2.0
        invalid-extension: "should fail"
        x-invalid_extension: "underscore not allowed"
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            ServerBindingsObject.model_validate(data)

        error_msg = str(exc_info.value)
        assert "does not match specification extension pattern" in error_msg

    def test_channel_bindings_invalid_extensions(self) -> None:
        """Test ChannelBindingsObject with invalid extensions."""

        yaml_data = """
        kafka:
          topic: test
          bindingVersion: 0.5.0
        not-x-prefix: "invalid"
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            ChannelBindingsObject.model_validate(data)

        error_msg = str(exc_info.value)
        assert "does not match specification extension pattern" in error_msg

    def test_operation_bindings_invalid_extensions(self) -> None:
        """Test OperationBindingsObject with invalid extensions."""

        yaml_data = """
        http:
          method: POST
          bindingVersion: 0.3.0
        x-invalid@symbol: "invalid char"
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            OperationBindingsObject.model_validate(data)

        error_msg = str(exc_info.value)
        assert "does not match specification extension pattern" in error_msg

    def test_message_bindings_invalid_extensions(self) -> None:
        """Test MessageBindingsObject with invalid extensions."""

        yaml_data = """
        http:
          headers:
            type: object
            properties:
              Content-Type:
                type: string
          bindingVersion: 0.3.0
        x-invalid extension: "space not allowed"
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            MessageBindingsObject.model_validate(data)

        error_msg = str(exc_info.value)
        assert "does not match specification extension pattern" in error_msg

    def test_server_bindings_extensions_serialization(self) -> None:
        """Test ServerBindingsObject extensions serialization round-trip."""
        yaml_data = """
        kafka:
          schemaRegistryUrl: https://test.com
          bindingVersion: 0.5.0
        x-test-extension: "test value"
        x-numeric-ext: 42
        x-bool-ext: true
        """
        data = yaml.safe_load(yaml_data)
        server_bindings = ServerBindingsObject.model_validate(data)

        # Serialize and deserialize
        dumped = server_bindings.model_dump()
        recreated = ServerBindingsObject.model_validate(dumped)

        # Check extensions are preserved
        assert recreated.model_extra is not None
        assert recreated.model_extra["x-test-extension"] == "test value"
        assert recreated.model_extra["x-numeric-ext"] == 42
        assert recreated.model_extra["x-bool-ext"] is True

    def test_channel_bindings_extensions_with_bindings(self) -> None:
        """Test ChannelBindingsObject with both bindings and extensions."""
        yaml_data = """
        kafka:
          topicConfiguration:
            cleanup.policy: ["delete"]
          bindingVersion: 0.5.0
        sqs:
          queue:
            name: test-queue
            fifoQueue: false
          bindingVersion: 0.3.0
        x-environment: "production"
        x-owner: "team-platform"
        """
        data = yaml.safe_load(yaml_data)
        channel_bindings = ChannelBindingsObject.model_validate(data)

        # Check bindings work normally
        assert channel_bindings.kafka is not None
        assert channel_bindings.sqs is not None
        assert channel_bindings.kafka.topic_configuration.cleanup_policy == ["delete"]

        # Check extensions
        assert channel_bindings.model_extra is not None
        assert channel_bindings.model_extra["x-environment"] == "production"
        assert channel_bindings.model_extra["x-owner"] == "team-platform"
