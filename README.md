# EDP — Encryption / Decryption Protocol (educational experiment)

**Status: Historical learning project — do not execute against real files.**

This repository documents an early experiment in symmetric and asymmetric encryption, file serialization, and recovery logic. It is preserved as a study of cryptographic APIs and the engineering risks of destructive file workflows.

> **Safety warning:** The current source contains operations that can modify, overwrite, and delete files. The application also launches background file-processing logic from its entry point. Do **not** execute, package, distribute, or test this version on a personal or organizational machine containing valuable data. Do not assume that files are recoverable after processing.

## Concepts explored

- Authenticated symmetric encryption using the `cryptography` library's Fernet interface.
- Public-key encryption for a symmetric data-encryption key.
- Combining serialized file metadata with content.
- File restoration and the risks of key management.

## Files

```text
EDP/
├── README.md
└── EDP/
    ├── edp.py         # experimental cryptographic and file-handling logic
    ├── ctkinter_.py   # graphical interface
    └── main.py        # application entry point
```

## Security and correctness limitations

This **is not a secure backup application or a production encryption protocol**. The current code has not been independently audited and includes destructive side effects. It makes assumptions about file locations, key material, metadata format, and recovery that must not be trusted for real data.

In particular:

- File operations and cryptographic operations are coupled.
- Restoration is not verified before destructive behavior can occur.
- Error handling can suppress important failures.
- File-path metadata must never be treated as safe input without validation.
- The current design lacks isolated, repeatable tests and a documented threat model.

## Future safe direction

A suitable follow-up project would be a **new, non-destructive cryptography laboratory** operating only on in-memory strings or disposable data in a dedicated sandbox. It should include explicit user consent, authenticated data formats, deterministic tests, and no automatic file deletion.

The purpose of publishing this code is to show the learning process and to make its limitations explicit. It should **not** be deployed.
