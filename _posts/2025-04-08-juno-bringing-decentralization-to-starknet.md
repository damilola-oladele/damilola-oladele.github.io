---
title: "Juno: Bringing decentralization to Starknet"
description: To mitigate the centralization risk posed by Starknet, Nethermind developed Juno, a Go implementation of Starknet’s full-node client.
date: 2025-04-07 00:00:00 +0100
categories: [Blockchain]
tags: [blockchain]
pin: false
image:
  path: /assets/img/cover-images/juno-bringing-decentralization-to-starknet.png
  alt: Cover image showing the title of post.
published: true
---

Blockchain is continually advancing in terms of scalability, security, and decentralization. However, improving all three at the same time presents a significant challenge. So most blockchains prioritize security and decentralization, often at the expense of scalability. This trade-off is particularly evident in Ethereum, where decentralization and security are maintained, but transaction throughput remains limited.

To address the scalability challenge, StarkWare, a software company specializing in cryptography, developed Starknet—a Layer 2 (L2) solution for Ethereum. Starknet uses **validity rollups**, also known as **zero-knowledge rollups (ZK-Rollups)**, to significantly increase transaction speed while inheriting Ethereum’s security.

Despite these advancements, Starknet relies on a centralized sequencer. This creates risks like downtime, transaction censorship, and a single point of failure. To mitigate these risks and push Starknet toward full decentralization, [Nethermind](https://www.nethermind.io/) developed [Juno](https://www.nethermind.io/juno), a Go implementation of Starknet’s full-node client.

So, what is Juno? What risks does Starknet present? How does Juno mitigate Starknet's risks? What are its key features, and how does it work? This post will answer all these questions.

A basic understanding of blockchain and Starknet will help you get the most out of this post.

Now, let's dive in.

## What is Juno?

Juno is an open-source Go implementation of Starknet full-node client, developed by Nethermind. It provides permissionless access to the Starknet ecosystem and supports various node setups. Over time, Juno aims to play a key role in decentralizing Starknet.

## What are the risks of Starknet?

Starknet currently relies on a single sequencer, raising concerns as it gives exclusive control of block production to a single entity. To understand why this is an issue, it’s important to examine the role of sequencers in Starknet’s ecosystem.

Similar to Ethereum’s validators, sequencers act as the backbone of Starknet. They collect, order, execute, and batch transactions into blocks. These blocks are then verified and submitted to Ethereum as a single proof. Unlike Ethereum’s validators, who secure the network, sequencers focus on transaction capacity, enabling Starknet to process high volumes efficiently.

However, this centralized control introduces risks such as:

* **Single points of failure:** If the sequencer experiences downtime or technical issues, the entire network stalls. Unlike decentralized blockchains, where multiple nodes keep operations running, Starknet’s current structure lacks backup mechanisms.  
* **Censorship risk:** A centralized sequencer gives a single entity significant power, allowing it to exclude transactions at its discretion. This undermines the core principles of decentralization and open access in blockchain.  
* **Limited client diversity:** Starknet’s ecosystem needs multiple independent full-node clients to prevent systemic failures. If all nodes run the same software, a bug could disrupt the entire network.

## How does Juno mitigate Starknet’s risks?

One of the reasons Juno is written in Go is to promote client diversity. Having multiple client implementations in different programming languages improves the network's stability. This way, bugs or vulnerabilities in one client are unlikely to impact the entire network, improving the overall security.

Additionally, Juno aims to decentralize Starknet’s infrastructure by reducing reliance on a single sequencer and providing an independent full-node client. Its decentralization roadmap consists of four phases. The first two are complete, the third is in progress, and the fourth is yet to be implemented:

**1\. Permissionless access to Starknet:** The first phase toward decentralization was permissionless access to Starknet’s blockchain data. Juno maintains a full copy of Starknet’s state, including blocks, transactions, contracts, and balances, retrieved from StarkWare’s API. It also verifies block and transaction hashes to ensure data integrity.

This phase laid the foundation for applications to interact with Starknet without relying on centralized services.

**2\. Full JSON-RPC support:** Juno expanded its capabilities by fully implementing the [**JSON-RPC specification**](https://github.com/starkware-libs/starknet-specs/tree/master). This lets developers access contract history, retrieve events, and estimate transaction fees. It also introduced Ethereum Layer 1 (L1) verification, ensuring Starknet’s state is accurately verified against Ethereum.

With this phase complete, Juno became production-ready for indexers, block explorers, and wallets.

**3\. Starknet decentralization begins:** This phase is currently in progress. It focuses on reducing reliance on Starknet’s centralized sequencer by enabling state synchronization between Juno full nodes.

To improve efficiency, Juno will implement Snap Sync, which lets new nodes sync quickly without downloading the entire historical state. Also, the JSON-RPC Trace API will help users better understand transaction execution.

While Juno will still forward transactions to the centralized sequencer for block inclusion, this phase is an important milestone in Starknet’s path to decentralization.

**4\. Juno as a Starknet sequencer:** The final phase in Juno’s decentralization roadmap is to become a sequencer that participates in L2 consensus. This will end the exclusive control over block production, distributing responsibility across multiple independent sequencers.

Once implemented, Juno will offer three modes of operation:

• **Light client:** fast, permissionless access with minimal verification  
• **Full node:** complete state verification and transaction execution  
• **Sequencer:** actively participates in the L2 consensus mechanism

## What are the key features of Juno?

The following features make Juno a critical component in Starknet’s path toward decentralization and scalability:

### Blockchain synchronization

Juno supports syncing with both Starknet **mainnet** and **testnet**, enabling users to access the latest blockchain data. It fully implements the JSON-RPC specification, offering full compatibility for read, write, and trace APIs. This ensures developers and applications can interact with Starknet when querying blocks, submitting transactions, or retrieving contract history.

### Advanced database optimizations

Juno incorporates several database optimizations that improve performance and storage efficiency:

* **Path-based trie storage:** Juno uses a path-based trie storage system for its state trie. This allows users to quickly retrieve contract storage data using the correct path and key. In contrast, node-based trie storage requires scanning the entire trie to find a hash, making it less efficient. The path-based system improves performance and reduces database size.  
* **Parallel root calculation:** Juno recalculates state trie roots in parallel, significantly increasing the speed of state updates. This method minimizes bottlenecks in blockchain state transitions, ensuring rapid synchronization.  
* **Lazy root recalculation:** Instead of recalculating the root of the state trie after every minor update, Juno applies all changes first and then recalculates the root only when necessary. This approach reduces redundant computations and optimizes processing efficiency.  
* **Mutable trie structure:** Juno adopts a mutable trie system, which minimizes storage requirements by modifying existing nodes instead of duplicating data. This structure helps reduce database size while maintaining fast access to blockchain state data.

### Ethereum L1 integration

Juno is designed to interact with Ethereum L1, ensuring accurate state tracking between Starknet and the Ethereum mainnet. It tracks Ethereum proofs to verify Starknet’s state consistency, allowing users to validate blockchain integrity without operating a full Ethereum node. This integration improves Starknet’s security and transparency. It also provides developers with a powerful tool for monitoring and verifying transactions on both L1 and L2.

### WebSocket interface

Juno provides a WebSocket RPC interface, enabling real-time blockchain monitoring by allowing users to subscribe to:

* New blocks  
* Transaction status changes  
* Pending transactions  
* Contract events

This feature is ideal for applications requiring instant notifications, such as wallets and trading platforms.

## How Juno works

Juno acts as an intermediary between users and the Starknet sequencer. Developers, decentralized applications (dApps), and businesses interact with Juno through its JSON-RPC and gRPC APIs. These interfaces provide access to Starknet’s blockchain data, enabling real-time queries, transaction submissions, and contract interactions.

Also, efficient synchronization is essential for Juno’s performance. To achieve this, it employs a three-stage syncing pipeline that ensures speed and accuracy:

1. **Download:** Juno retrieves blocks and state diffs from Starknet’s sequencer, eliminating the need for local transaction execution.  
2. **Sanity checks:** Juno verifies block hashes and confirms data integrity to detect any inconsistencies before applying updates.  
3. **Full verification:** Juno applies state updates and validates the correctness of the new state root, ensuring the blockchain data remains consistent.

Additionally, Juno integrates parallelized block verification, enabling concurrent processing of multiple blocks, which improves synchronization speed.

## Conclusion

Decentralization isn’t just an improvement, it’s the foundation of a secure and resilient blockchain network. A system controlled by a single entity introduces risks such as a single point of failure, network downtime, and transaction censorship. Juno addresses these risks by distributing power across multiple nodes, ensuring Starknet remains open, permissionless, and reliable.

Juno is more than just a full-node solution, it’s a step toward full decentralization, where no single entity dictates transaction processing. With advanced synchronization, database optimizations, and Ethereum L1 integration, Juno lays the groundwork for a future where Starknet operates without centralized bottlenecks.

Want to contribute or learn more about Juno? Check out [Juno on GitHub](https://github.com/NethermindEth/juno).
