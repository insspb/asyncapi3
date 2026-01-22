"""Managers for handling reusable operation objects in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["OperationsManager"]


from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.models.components import Components
from asyncapi3.models.operation import Operation, Operations
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class OperationsManager(ProcessorProtocol):
    """
    Manager for handling Operation objects in AsyncAPI specification.

    This manager ensures that all Operation objects are stored in components/operations
    and replaced with Reference objects throughout the specification.
    Duplicate operations with the same name are not allowed.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process operations in the AsyncAPI specification.

        Moves all operations from root to components/operations, replaces them with
        references, and ensures no duplicate operation names exist.

        Args:
            spec: The AsyncAPI3 specification to process

        Returns:
            The modified AsyncAPI3 specification
        """
        self._ensure_components_operations_exist(spec)

        self._process_root_operations(spec)

        return spec

    def _ensure_components_operations_exist(self, spec: AsyncAPI3) -> None:
        """
        Ensure that components and operations section exist in the specification.

        Creates components with operations if components doesn't exist.
        Adds operations to existing components if operations section is missing.
        """
        if not spec.components:
            spec.components = Components(operations=Operations({}))
        elif not spec.components.operations:
            spec.components.operations = Operations({})

    def _process_root_operations(self, spec: AsyncAPI3) -> None:
        """Process operations in the root operations object."""
        if not spec.operations:
            return

        processed_operations: dict[str, Operation | Reference] = {}

        for operation_name, operation in spec.operations.root.items():
            if isinstance(operation, Reference):
                processed_operations[operation_name] = operation
                continue

            if isinstance(operation, Operation):
                self._ensure_is_unique_operation(spec, operation_name, operation)
                self._add_operation_to_components(spec, operation_name, operation)
                processed_operations[operation_name] = (
                    Reference.to_component_operation_name(operation_name)
                )

        spec.operations.root = processed_operations

    def _ensure_is_unique_operation(
        self,
        spec: AsyncAPI3,
        operation_name: str,
        operation: Operation | Reference,
    ) -> None:
        """
        Ensure that an operation with the given name is unique.

        Args:
            spec: The AsyncAPI3 specification
            operation_name: Name/key for the operation to check
            operation: Operation object to validate for uniqueness

        Raises:
            ValueError: If an operation with the same name but different content already
                exists
        """
        if (
            not spec.components or not spec.components.operations
        ):  # mypy types protection
            return

        if operation_name in spec.components.operations.root:
            existing_operation = spec.components.operations.root[operation_name]
            if existing_operation != operation:
                raise ValueError(
                    f"Operation name conflict detected: '{operation_name}' exists "
                    "with different content. "
                    f"Existing: {existing_operation.model_dump()}, "
                    f"New: {operation.model_dump()}. Operation names must be unique."
                )
            return

    def _add_operation_to_components(
        self,
        spec: AsyncAPI3,
        operation_name: str,
        operation: Operation,
    ) -> None:
        """
        Add an operation to the components/operations section.

        Args:
            spec: The AsyncAPI3 specification
            operation_name: Name/key for the operation
            operation: Operation object to add
        """
        spec.components.operations.root[operation_name] = operation  # type: ignore[union-attr]
