/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     END_OF_FILE = 0,
     PREC_BOT = 258,
     REPEAT = 259,
     ALTERNATIVE = 260,
     COMPOSITE = 261,
     ADDLYRICS = 262,
     DURATION_IDENTIFIER = 263,
     EXTENDER = 264,
     HYPHEN = 265,
     EVENT_FUNCTION = 266,
     EVENT_IDENTIFIER = 267,
     E_UNSIGNED = 268,
     REAL = 269,
     UNSIGNED = 270,
     NUMBER_IDENTIFIER = 271,
     PREC_TOP = 272,
     ACCEPTS = 273,
     ALIAS = 274,
     BOOK = 275,
     BOOKPART = 276,
     CHANGE = 277,
     CHORDMODE = 278,
     CHORDS = 279,
     CONSISTS = 280,
     CONTEXT = 281,
     DEFAULT = 282,
     DEFAULTCHILD = 283,
     DENIES = 284,
     DESCRIPTION = 285,
     DRUMMODE = 286,
     DRUMS = 287,
     ETC = 288,
     FIGUREMODE = 289,
     FIGURES = 290,
     HEADER = 291,
     INVALID = 292,
     LAYOUT = 293,
     LYRICMODE = 294,
     LYRICS = 295,
     LYRICSTO = 296,
     MARKUP = 297,
     MARKUPLIST = 298,
     MIDI = 299,
     NAME = 300,
     NOTEMODE = 301,
     OVERRIDE = 302,
     PAPER = 303,
     REMOVE = 304,
     REST = 305,
     REVERT = 306,
     SCORE = 307,
     SCORELINES = 308,
     SEQUENTIAL = 309,
     SET = 310,
     SIMULTANEOUS = 311,
     TEMPO = 312,
     TYPE = 313,
     UNSET = 314,
     WITH = 315,
     NEWCONTEXT = 316,
     CHORD_BASS = 317,
     CHORD_CARET = 318,
     CHORD_COLON = 319,
     CHORD_MINUS = 320,
     CHORD_SLASH = 321,
     ANGLE_OPEN = 322,
     ANGLE_CLOSE = 323,
     DOUBLE_ANGLE_OPEN = 324,
     DOUBLE_ANGLE_CLOSE = 325,
     E_BACKSLASH = 326,
     E_EXCLAMATION = 327,
     E_PLUS = 328,
     FIGURE_CLOSE = 329,
     FIGURE_OPEN = 330,
     FIGURE_SPACE = 331,
     MULTI_MEASURE_REST = 332,
     EXPECT_MARKUP = 333,
     EXPECT_SCM = 334,
     BACKUP = 335,
     REPARSE = 336,
     EXPECT_MARKUP_LIST = 337,
     EXPECT_OPTIONAL = 338,
     EXPECT_NO_MORE_ARGS = 339,
     EMBEDDED_LILY = 340,
     BOOK_IDENTIFIER = 341,
     CHORD_MODIFIER = 342,
     CHORD_REPETITION = 343,
     CONTEXT_MOD_IDENTIFIER = 344,
     DRUM_PITCH = 345,
     PITCH_IDENTIFIER = 346,
     FRACTION = 347,
     LYRIC_ELEMENT = 348,
     MARKUP_FUNCTION = 349,
     MARKUP_LIST_FUNCTION = 350,
     MARKUP_IDENTIFIER = 351,
     MARKUPLIST_IDENTIFIER = 352,
     MUSIC_FUNCTION = 353,
     MUSIC_IDENTIFIER = 354,
     NOTENAME_PITCH = 355,
     RESTNAME = 356,
     SCM_ARG = 357,
     SCM_FUNCTION = 358,
     SCM_IDENTIFIER = 359,
     SCM_TOKEN = 360,
     STRING = 361,
     SYMBOL_LIST = 362,
     TONICNAME_PITCH = 363,
     UNARY_MINUS = 364
   };
#endif
/* Tokens.  */
#define END_OF_FILE 0
#define PREC_BOT 258
#define REPEAT 259
#define ALTERNATIVE 260
#define COMPOSITE 261
#define ADDLYRICS 262
#define DURATION_IDENTIFIER 263
#define EXTENDER 264
#define HYPHEN 265
#define EVENT_FUNCTION 266
#define EVENT_IDENTIFIER 267
#define E_UNSIGNED 268
#define REAL 269
#define UNSIGNED 270
#define NUMBER_IDENTIFIER 271
#define PREC_TOP 272
#define ACCEPTS 273
#define ALIAS 274
#define BOOK 275
#define BOOKPART 276
#define CHANGE 277
#define CHORDMODE 278
#define CHORDS 279
#define CONSISTS 280
#define CONTEXT 281
#define DEFAULT 282
#define DEFAULTCHILD 283
#define DENIES 284
#define DESCRIPTION 285
#define DRUMMODE 286
#define DRUMS 287
#define ETC 288
#define FIGUREMODE 289
#define FIGURES 290
#define HEADER 291
#define INVALID 292
#define LAYOUT 293
#define LYRICMODE 294
#define LYRICS 295
#define LYRICSTO 296
#define MARKUP 297
#define MARKUPLIST 298
#define MIDI 299
#define NAME 300
#define NOTEMODE 301
#define OVERRIDE 302
#define PAPER 303
#define REMOVE 304
#define REST 305
#define REVERT 306
#define SCORE 307
#define SCORELINES 308
#define SEQUENTIAL 309
#define SET 310
#define SIMULTANEOUS 311
#define TEMPO 312
#define TYPE 313
#define UNSET 314
#define WITH 315
#define NEWCONTEXT 316
#define CHORD_BASS 317
#define CHORD_CARET 318
#define CHORD_COLON 319
#define CHORD_MINUS 320
#define CHORD_SLASH 321
#define ANGLE_OPEN 322
#define ANGLE_CLOSE 323
#define DOUBLE_ANGLE_OPEN 324
#define DOUBLE_ANGLE_CLOSE 325
#define E_BACKSLASH 326
#define E_EXCLAMATION 327
#define E_PLUS 328
#define FIGURE_CLOSE 329
#define FIGURE_OPEN 330
#define FIGURE_SPACE 331
#define MULTI_MEASURE_REST 332
#define EXPECT_MARKUP 333
#define EXPECT_SCM 334
#define BACKUP 335
#define REPARSE 336
#define EXPECT_MARKUP_LIST 337
#define EXPECT_OPTIONAL 338
#define EXPECT_NO_MORE_ARGS 339
#define EMBEDDED_LILY 340
#define BOOK_IDENTIFIER 341
#define CHORD_MODIFIER 342
#define CHORD_REPETITION 343
#define CONTEXT_MOD_IDENTIFIER 344
#define DRUM_PITCH 345
#define PITCH_IDENTIFIER 346
#define FRACTION 347
#define LYRIC_ELEMENT 348
#define MARKUP_FUNCTION 349
#define MARKUP_LIST_FUNCTION 350
#define MARKUP_IDENTIFIER 351
#define MARKUPLIST_IDENTIFIER 352
#define MUSIC_FUNCTION 353
#define MUSIC_IDENTIFIER 354
#define NOTENAME_PITCH 355
#define RESTNAME 356
#define SCM_ARG 357
#define SCM_FUNCTION 358
#define SCM_IDENTIFIER 359
#define SCM_TOKEN 360
#define STRING 361
#define SYMBOL_LIST 362
#define TONICNAME_PITCH 363
#define UNARY_MINUS 364




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif



#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
} YYLTYPE;
# define yyltype YYLTYPE /* obsolescent; will be withdrawn */
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


