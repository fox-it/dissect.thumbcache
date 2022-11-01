from dissect.cstruct import cstruct

c_thumbcache_index_def = """
struct INDEX_HEADER_V1 {
    char    Signature[4];
    uint32  Version;
    uint32  Unknown1;
    uint32  UsedEntries;
    uint32  TotalEntries;
    uint32  Unknown2;
};

struct INDEX_HEADER_V2 {
    char    Signature[8];  // 0x00
    uint64  Version;       // 0x08
    uint32  Unknown1;      // 0x10
    uint32  UsedEntries;  // 0x14
    uint32  TotalEntries; // 0x18
    uint32  Unknown2;      // 0x1B
}; // 0x20

struct VISTA_ENTRY {
    char    Hash[8];
    uint64  LastModified;
    uint32  Flags;
};

struct WINDOWS7_ENTRY {
    char    Hash[8];
    uint32  Flags;
};

struct WINDOWS8_ENTRY {
    char    Hash[8];
    uint32  Flags;
    uint32  Unknown; // Is sometimes filled with information, couldn't figure out what it meant yet though.
};

struct CACHE_HEADER {
    char    Signature[4];
    uint32  Version;
    uint32  Type;
    uint32  Size;
    uint32  Offset;
    uint32  Entries;
};

struct CACHE_HEADER_VISTA {
    char    Signature[4];
    uint32  Version;
    uint32  Type;
    uint32  Offset;
    uint32  Size;
    uint32  Entries;
};

struct CACHE_ENTRY {
    char    Signature[4];
    uint32  Size;
    char    Hash[8];
    uint32  IdentifierSize;
    uint32  PaddingSize;
    uint32  DataSize;
    uint32  Unknown;
};

struct CACHE_ENTRY_VISTA {
    char    Signature[4];
    uint32  Size;
    char    Hash[8];
    wchar   Extension[4];
    uint32  IdentifierSize;
    uint32  PaddingSize;
    uint32  DataSize;
    uint32  Unknown;
};
"""
c_thumbcache_index = cstruct()
c_thumbcache_index.load(c_thumbcache_index_def)
