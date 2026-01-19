"""Tests for managers."""

from _pytest.logging import LogCaptureFixture

from asyncapi3.managers import TagsManager
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.base import Reference, Tag


class TestTagsManager:
    """Tests for TagsManager."""

    def test_tag_manager_processes_info_tags(self) -> None:
        """Test TagsManager processes tags in info section."""
        # Create spec with duplicate tags in info
        spec = AsyncAPI3.as_builder(
            title="Test API",
            tags=[
                Tag(name="tag1", description="First tag"),
                Tag(name="tag2", description="Second tag"),
                Tag(name="tag1", description="First tag"),  # Duplicate
            ],
        )

        # After model validation and TagsManager processing, tags should be deduplicated,
        # moved to components and replaced with references
        spec_data = spec.model_dump()
        assert "tags" in spec_data["components"]
        assert len(spec_data["components"]["tags"]) == 2  # Only unique tags

        # Info tags should be references, only unique ones preserved
        assert len(spec_data["info"]["tags"]) == 2  # Only unique tags present
        # Check that references point to components
        for tag_ref in spec_data["info"]["tags"]:
            assert "$ref" in tag_ref
            assert tag_ref["$ref"].startswith("#/components/tags/")

    def test_tag_manager_processes_server_tags(self) -> None:
        """Test TagsManager processes tags in servers."""
        tag1 = Tag(name="env:prod", description="Production")
        tag2 = Tag(name="env:stage", description="Staging")

        spec = AsyncAPI3.as_builder(
            title="Test API",
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "tags": [tag1],
                },
                "stage": {
                    "host": "stage.api.example.com",
                    "protocol": "https",
                    "tags": [tag2, tag1],  # Duplicate across servers
                },
            },
        )

        spec_data = spec.model_dump()

        # Tags should be in components
        assert "tags" in spec_data["components"]
        assert len(spec_data["components"]["tags"]) == 2

        # Server tags should be references
        for _server_name, server_data in spec_data["servers"].items():
            if "tags" in server_data:
                for tag_ref in server_data["tags"]:
                    assert "$ref" in tag_ref
                    assert tag_ref["$ref"].startswith("#/components/tags/")

    def test_tag_manager_avoids_duplicates_across_objects(self) -> None:
        """Test TagsManager avoids duplicates across different objects."""
        shared_tag = Tag(name="shared", description="Shared tag")

        spec = AsyncAPI3.as_builder(
            title="Test API",
            tags=[shared_tag],
            servers={
                "server1": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "tags": [shared_tag],  # Same tag instance
                },
            },
        )

        spec_data = spec.model_dump()

        # Only one instance in components
        assert len(spec_data["components"]["tags"]) == 1

        # All references should point to the same component
        info_ref = spec_data["info"]["tags"][0]["$ref"]
        server_ref = spec_data["servers"]["server1"]["tags"][0]["$ref"]
        assert info_ref == server_ref

    def test_tag_manager_handles_empty_tags(self) -> None:
        """Test TagsManager handles objects without tags."""
        spec = AsyncAPI3.as_builder(
            title="Test API",
            servers={
                "server1": {
                    "host": "api.example.com",
                    "protocol": "https",
                },
            },
        )

        spec_data = spec.model_dump()

        # No tags in components initially
        assert spec_data["components"]["tags"] == {}

        # Server should not have tags field
        assert "tags" not in spec_data["servers"]["server1"]

    def test_tag_manager_preserves_references(self) -> None:
        """Test TagsManager preserves existing references."""
        ref = Reference.to_component_tag_name("existing_tag")

        spec = AsyncAPI3.as_builder(
            title="Test API",
            tags=[ref],  # Already a reference
        )

        spec_data = spec.model_dump()

        # Reference should be preserved
        assert spec_data["info"]["tags"][0]["$ref"] == "#/components/tags/existing_tag"

    def test_tag_manager_with_manual_initialization(self) -> None:
        """Test TagsManager works when manually added to extra_converters."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [
                    Tag(name="manual", description="Manual tag"),
                ],
            },
            components={
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec_data = spec.model_dump()

        # Tag should be moved to components
        assert "tags" in spec_data["components"]
        assert len(spec_data["components"]["tags"]) == 1

        # Info should have reference
        assert len(spec_data["info"]["tags"]) == 1
        assert "$ref" in spec_data["info"]["tags"][0]

    def test_tag_manager_creates_components_when_missing(self) -> None:
        """Test TagsManager creates components and tags sections when they don't exist."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [
                    Tag(name="test", description="Test tag"),
                ],
            },
            # No components section
            extra_converters=[TagsManager],
        )

        # Manually run processors since this is not using as_builder
        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Components should be created with tags
        assert "components" in spec_data
        assert "tags" in spec_data["components"]
        assert len(spec_data["components"]["tags"]) == 1
        assert "test" in spec_data["components"]["tags"]

        # Info should have reference
        assert len(spec_data["info"]["tags"]) == 1
        assert "$ref" in spec_data["info"]["tags"][0]

    def test_tag_manager_creates_tags_when_components_exist_without_tags(self) -> None:
        """Test TagsManager creates tags section when components exists but tags don't."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [
                    Tag(name="test", description="Test tag"),
                ],
            },
            components={
                "schemas": {},
                # No tags section
            },
            extra_converters=[TagsManager],
        )

        # Manually run processors
        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Tags should be added to existing components
        assert "components" in spec_data
        assert "tags" in spec_data["components"]
        assert "schemas" in spec_data["components"]  # Existing section preserved
        assert len(spec_data["components"]["tags"]) == 1
        assert "test" in spec_data["components"]["tags"]

    def test_tag_manager_handles_tag_name_conflicts(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test TagsManager logs warning for tag name conflicts with different content."""
        # Create tags with same name but different descriptions
        tag1 = Tag(name="env:prod", description="Production environment")
        tag2 = Tag(
            name="env:prod", description="Different description"
        )  # Same name, different content

        spec = AsyncAPI3.as_builder(
            title="Test API",
            tags=[tag1],
            servers={
                "server1": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "tags": [tag2],  # Tag with same name but different content
                },
            },
        )

        # Check that warning was logged
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "WARNING"
        assert "Tag name conflict detected" in caplog.records[0].message
        assert "env:prod" in caplog.records[0].message

        spec_data = spec.model_dump()

        # Only one tag should be in components (first one encountered)
        assert len(spec_data["components"]["tags"]) == 1
        assert "env:prod" in spec_data["components"]["tags"]
        assert (
            spec_data["components"]["tags"]["env:prod"]["description"]
            == "Production environment"
        )

        # Both references should point to the same component
        info_ref = spec_data["info"]["tags"][0]["$ref"]
        server_ref = spec_data["servers"]["server1"]["tags"][0]["$ref"]
        assert info_ref == server_ref == "#/components/tags/env:prod"

    def test_tag_manager_processes_root_channel_tags(self) -> None:
        """Test TagsManager processes tags in root channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "root_channel": {
                    "address": "/root",
                    "messages": {},
                    "tags": [
                        Tag(name="root_channel", description="Root channel"),
                    ],
                }
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert len(spec_data["channels"]["root_channel"]["tags"]) == 1
        tag_ref = spec_data["channels"]["root_channel"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/root_channel"

    def test_tag_manager_processes_root_operation_tags(self) -> None:
        """Test TagsManager processes tags in root operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "root_operation": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "tags": [
                        Tag(name="root_operation", description="Root operation"),
                    ],
                }
            },
            channels={"test": {"address": "/test"}},
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert len(spec_data["operations"]["root_operation"]["tags"]) == 1
        tag_ref = spec_data["operations"]["root_operation"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/root_operation"

    def test_tag_manager_processes_components_messages_tags(self) -> None:
        """Test TagsManager processes tags in messages stored in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "messages": {
                    "comp_message": {
                        "payload": {"type": "string"},
                        "tags": [
                            Tag(name="comp_message", description="Component message"),
                        ],
                    }
                },
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert len(spec_data["components"]["messages"]["comp_message"]["tags"]) == 1
        tag_ref = spec_data["components"]["messages"]["comp_message"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/comp_message"

    def test_tag_manager_processes_operations_messages_tags(self) -> None:
        """Test TagsManager processes tags in messages within root operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "operation_with_messages": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "messages": [{"$ref": "#/components/messages/test_message"}],
                }
            },
            channels={"test": {"address": "/test"}},
            components={
                "messages": {
                    "test_message": {
                        "payload": {"type": "string"},
                        "tags": [
                            Tag(
                                name="operation_message",
                                description="Message within operation",
                            ),
                        ],
                    }
                }
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed in the message
        message = spec_data["components"]["messages"]["test_message"]
        assert len(message["tags"]) == 1
        tag_ref = message["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/operation_message"

    def test_tag_manager_processes_operation_traits_without_tags(self) -> None:
        """Test TagsManager handles operation traits without tags."""

        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "operation_with_trait": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "traits": [
                        {
                            "title": "Trait without tags",
                            # No tags field
                        }
                    ],
                }
            },
            channels={"test": {"address": "/test"}},
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that trait is preserved
        operation = spec_data["operations"]["operation_with_trait"]
        assert len(operation["traits"]) == 1
        trait = operation["traits"][0]
        assert trait["title"] == "Trait without tags"
        assert "tags" not in trait

    def test_tag_manager_processes_operation_traits_with_empty_tags(self) -> None:
        """Test TagsManager handles operation traits with empty tags list."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "operation_with_trait": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "traits": [
                        {
                            "title": "Trait with empty tags",
                            "tags": [],  # Empty tags list
                        }
                    ],
                }
            },
            channels={"test": {"address": "/test"}},
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that trait is preserved with empty tags
        operation = spec_data["operations"]["operation_with_trait"]
        assert len(operation["traits"]) == 1
        trait = operation["traits"][0]
        assert trait["title"] == "Trait with empty tags"
        assert trait["tags"] == []

    def test_tag_manager_processes_operation_traits_with_references(self) -> None:
        """Test TagsManager handles operation traits with reference objects."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "operation_with_trait": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "traits": [
                        {"$ref": "#/components/operationTraits/trait_ref"},
                        {
                            "title": "Trait with tags",
                            "tags": [
                                Tag(name="trait_tag", description="Tag in trait"),
                            ],
                        },
                    ],
                }
            },
            channels={"test": {"address": "/test"}},
            components={
                "operationTraits": {
                    "trait_ref": {
                        "title": "Referenced trait",
                    }
                },
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that both reference and trait are preserved
        operation = spec_data["operations"]["operation_with_trait"]
        assert len(operation["traits"]) == 2

        # First trait is a reference
        ref_trait = operation["traits"][0]
        assert "$ref" in ref_trait
        assert ref_trait["$ref"] == "#/components/operationTraits/trait_ref"

        # Second trait has processed tags
        tag_trait = operation["traits"][1]
        assert tag_trait["title"] == "Trait with tags"
        assert len(tag_trait["tags"]) == 1
        tag_ref = tag_trait["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/trait_tag"

    def test_tag_manager_processes_components_servers_tags(self) -> None:
        """Test TagManager processes tags in servers stored in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "servers": {
                    "comp_server": {
                        "host": "comp.example.com",
                        "protocol": "https",
                        "tags": [
                            Tag(name="comp", description="Component server"),
                            Tag(name="shared", description="Shared tag"),
                        ],
                    }
                },
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert len(spec_data["components"]["servers"]["comp_server"]["tags"]) == 2
        for tag_ref in spec_data["components"]["servers"]["comp_server"]["tags"]:
            assert "$ref" in tag_ref
            assert tag_ref["$ref"].startswith("#/components/tags/")

        # Check that tags are in components
        assert len(spec_data["components"]["tags"]) == 2

    def test_tag_manager_processes_components_channels_tags(self) -> None:
        """Test TagManager processes tags in channels stored in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "channels": {
                    "comp_channel": {
                        "address": "/comp",
                        "messages": {},
                        "tags": [
                            Tag(name="comp_channel", description="Component channel"),
                        ],
                    }
                },
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert len(spec_data["components"]["channels"]["comp_channel"]["tags"]) == 1
        tag_ref = spec_data["components"]["channels"]["comp_channel"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/comp_channel"

    def test_tag_manager_processes_components_operations_tags(self) -> None:
        """Test TagManager processes tags in operations stored in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "operations": {
                    "comp_operation": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/test"},
                        "tags": [
                            Tag(
                                name="comp_operation", description="Component operation"
                            ),
                        ],
                    }
                },
                "channels": {"test": {"address": "/test"}},
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert len(spec_data["components"]["operations"]["comp_operation"]["tags"]) == 1
        tag_ref = spec_data["components"]["operations"]["comp_operation"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/comp_operation"

    def test_tag_manager_processes_components_operation_traits_tags(self) -> None:
        """Test TagManager processes tags in operation traits stored in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "operationTraits": {
                    "comp_trait": {
                        "tags": [
                            Tag(
                                name="comp_trait",
                                description="Component operation trait",
                            ),
                        ]
                    }
                },
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert (
            len(spec_data["components"]["operationTraits"]["comp_trait"]["tags"]) == 1
        )
        tag_ref = spec_data["components"]["operationTraits"]["comp_trait"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/comp_trait"

    def test_tag_manager_processes_components_message_traits_tags(self) -> None:
        """Test TagManager processes tags in message traits stored in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "messageTraits": {
                    "comp_msg_trait": {
                        "tags": [
                            Tag(
                                name="comp_msg_trait",
                                description="Component message trait",
                            ),
                        ]
                    }
                },
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags are processed
        assert (
            len(spec_data["components"]["messageTraits"]["comp_msg_trait"]["tags"]) == 1
        )
        tag_ref = spec_data["components"]["messageTraits"]["comp_msg_trait"]["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/comp_msg_trait"

    def test_tag_manager_processes_operation_traits(self) -> None:
        """Test TagManager processes tags in operation traits."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "test_operation": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "traits": [
                        {
                            "tags": [
                                Tag(
                                    name="operation_trait_tag",
                                    description="Tag in operation trait",
                                ),
                            ]
                        }
                    ],
                }
            },
            channels={"test": {"address": "/test"}},
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags in operation traits are processed
        operation = spec_data["operations"]["test_operation"]
        assert "traits" in operation
        assert len(operation["traits"]) == 1

        trait = operation["traits"][0]
        assert "tags" in trait
        assert len(trait["tags"]) == 1

        tag_ref = trait["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/operation_trait_tag"

    def test_tag_manager_processes_components_operation_traits(self) -> None:
        """Test TagManager processes tags in operation traits within components operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "operations": {
                    "comp_operation": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/test"},
                        "traits": [
                            {
                                "tags": [
                                    Tag(
                                        name="comp_operation_trait_tag",
                                        description="Tag in component operation trait",
                                    ),
                                ]
                            }
                        ],
                    }
                },
                "channels": {"test": {"address": "/test"}},
                "tags": {},
            },
            extra_converters=[TagsManager],
        )

        spec.run_extra_processors()  # type: ignore[operator]

        spec_data = spec.model_dump()

        # Check that tags in component operation traits are processed
        operation = spec_data["components"]["operations"]["comp_operation"]
        assert "traits" in operation
        assert len(operation["traits"]) == 1

        trait = operation["traits"][0]
        assert "tags" in trait
        assert len(trait["tags"]) == 1

        tag_ref = trait["tags"][0]
        assert "$ref" in tag_ref
        assert tag_ref["$ref"] == "#/components/tags/comp_operation_trait_tag"
