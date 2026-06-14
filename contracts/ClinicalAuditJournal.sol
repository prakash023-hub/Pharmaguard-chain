// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ClinicalAuditJournal — immutable agent decision log for Mantle Turing Test 2026
/// @notice Agentic Economy track: RealClaw real-life expansion (healthcare, not DeFi)
contract ClinicalAuditJournal {
    struct Decision {
        bytes32 queryHash;
        bytes32 recommendationHash;
        string awareCategory;
        uint256 timestamp;
        address agent;
    }

    mapping(bytes32 => Decision) public decisions;
    bytes32[] public decisionIds;
    address public owner;

    event DecisionLogged(
        bytes32 indexed decisionId,
        address indexed agent,
        string awareCategory,
        uint256 timestamp
    );

    constructor() {
        owner = msg.sender;
    }

    function logDecision(
        bytes32 queryHash,
        bytes32 recommendationHash,
        string calldata awareCategory
    ) external returns (bytes32 decisionId) {
        decisionId = keccak256(
            abi.encodePacked(queryHash, recommendationHash, block.timestamp, msg.sender)
        );
        decisions[decisionId] = Decision({
            queryHash: queryHash,
            recommendationHash: recommendationHash,
            awareCategory: awareCategory,
            timestamp: block.timestamp,
            agent: msg.sender
        });
        decisionIds.push(decisionId);
        emit DecisionLogged(decisionId, msg.sender, awareCategory, block.timestamp);
    }

    function decisionCount() external view returns (uint256) {
        return decisionIds.length;
    }
}
