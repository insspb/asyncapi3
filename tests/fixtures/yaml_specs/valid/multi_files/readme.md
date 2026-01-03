# Small social media example

Say we have a social network, a very basic one, where all you can do is upvoting
comments.

The individual services are defined as such:

- [A frontend application (./frontend)](./frontend/asyncapi.yaml) where users interact
  through the website, where they can like comments.
- [A backend WebSocket server (./backend)](./backend/asyncapi.yaml) that sends and
  receives events for the UI to update in real-time.
- [A comment service (./comments-service)](./comments-service/asyncapi.yaml) which
  processes all events related to comments through a message broker.
- [A notification service (./notification-service)](./notification-service/asyncapi.yaml)
  which ensures all relevant parties to the comment is notified.
- [A public-facing API (./public-api)](./public-api/asyncapi.yaml) which is an external
  application, where anyone outside the organization can get notified about updates.

This ensures that we try to describe the following use-cases mixed together:

- A public API, and how others may interact with our system.
- A broker setup to include the most widely used scenario
- A WebSocket server and client to ensure we dont focus only on broker centric systems.
- Reusability where possible, to ensure no dublication of definitions
