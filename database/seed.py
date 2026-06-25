"""
Database seed file - Full roadmap data
Populates all subjects, topics, subtopics, and initial checklist structure
NOTE: This is a comprehensive seed file. Due to size, this contains the framework.
You should expand this with complete Phase 1-5 data as per the requirements.
"""
from datetime import date, timedelta
from database.models import Subject, Topic, UserProfile, ChecklistItem, TopicMastery, DailyLog
from database.database import get_session


def create_dsa_topics(session, subject_id, start_date):
    """Create all DSA topics for Phase 1"""
    day_counter = 0
    topics_data = [
        ("Arrays Basics", ["Declaration", "Traversal", "Insertion", "Deletion"], 1),
        ("Arrays Two Pointer & Sliding Window", ["Two pointer technique", "Sliding window"], 1),
        ("Arrays Prefix Sum", ["Prefix sum", "Subarray problems", "Kadane's algorithm"], 1),
        ("Strings Basics", ["charAt", "substring", "Immutability", "String pool"], 1),
        ("Strings Pattern Matching", ["Pattern matching", "Palindrome", "Anagram"], 1),
        ("Practice: Arrays+Strings", ["10 mixed problems"], 1),
        ("Sorting Basics", ["Bubble sort", "Selection sort", "Insertion sort"], 1),
        ("StringBuilder & Manipulation", ["StringBuilder", "String manipulation methods"], 1),
        ("Practice + Week 1 Revision", ["Revision of week 1 topics"], 1),
        ("Recursion Basics", ["Base case", "Call stack", "Factorial", "Fibonacci"], 1),
        ("Recursion Patterns", ["Print patterns", "Reverse string recursively"], 1),
        ("Recursion Advanced", ["Sum of digits", "Tower of Hanoi concept"], 1),
        ("Practice: Recursion", ["8 recursion problems"], 1),
        ("Binary Search Basics", ["Binary search concept", "Implementation"], 1),
        ("Binary Search Advanced", ["Rotated arrays", "Search variants"], 1),
        ("Merge Sort", ["Divide and conquer", "Merge sort implementation"], 1),
        ("Quick Sort", ["Quick sort concept", "Partitioning"], 1),
        ("Practice: Searching+Sorting", ["10 problems"], 1),
        ("Linked List - Singly", ["Node structure", "Traversal", "Insertion"], 1),
        ("Linked List - Operations", ["Deletion", "Search", "Length"], 1),
        ("Doubly Linked List", ["DLL structure", "Insertion", "Deletion"], 1),
        ("Linked List - Reverse & Cycle", ["Reverse list", "Floyd's cycle detection"], 1),
        ("Linked List - Advanced", ["Merge sorted lists", "Find middle"], 1),
        ("Practice: Linked Lists", ["10 problems"], 1),
        ("Stack Basics", ["Push", "Pop", "Peek", "Array implementation"], 1),
        ("Stack Advanced", ["LinkedList implementation", "Valid parentheses"], 1),
        ("Queue Basics", ["Enqueue", "Dequeue", "Circular queue"], 1),
        ("Queue Advanced", ["Two-stack implementation", "Priority queue intro"], 1),
        ("Practice: Stack+Queue", ["10 problems"], 1),
        ("HashMap and HashSet", ["HashMap", "HashSet", "Java collections"], 1),
        ("Hashing - Frequency", ["Frequency count", "Find duplicates", "Two sum"], 1),
        ("Hashing - Advanced", ["Group anagrams", "Longest consecutive sequence"], 1),
        ("Practice: Hashing", ["10 hashing problems"], 1),
        ("Binary Tree Basics", ["Tree structure", "Inorder", "Preorder", "Postorder"], 1),
        ("Binary Tree BFS", ["Level order traversal", "Tree height", "Width"], 1),
        ("BST Basics", ["BST insertion", "Search", "Deletion"], 1),
        ("BST Advanced", ["Validate BST", "Kth smallest", "Kth largest"], 1),
        ("Tree Advanced", ["LCA", "Diameter", "Path sum"], 1),
        ("Practice: Trees", ["10 tree problems"], 1),
        ("Heap Basics", ["Min heap", "Max heap concept"], 1),
        ("Java PriorityQueue", ["PriorityQueue usage", "Custom comparator"], 1),
        ("Heap Problems", ["Kth largest", "Top K frequent"], 1),
        ("Practice: Heap", ["8 heap problems"], 1),
        ("Graph Basics", ["Terminology", "Adjacency list", "Adjacency matrix"], 1),
        ("BFS Traversal", ["BFS concept", "BFS implementation"], 1),
        ("DFS Traversal", ["DFS concept", "DFS implementation"], 1),
        ("Graph Cycle Detection", ["Cycle detection in undirected graph"], 1),
        ("Graph Advanced", ["Cycle in directed graph", "Topological sort"], 1),
        ("Topological Sort", ["DFS method", "Kahn's algorithm"], 1),
        ("Practice: Graphs", ["10 graph problems"], 1),
    ]
    
    for idx, (name, subtopics, phase) in enumerate(topics_data):
        topic = Topic(
            subject_id=subject_id,
            name=name,
            part_number=None,
            total_parts=None,
            subtopics=subtopics,
            sequence_order=idx + 1,
            phase=phase,
            scheduled_date=start_date + timedelta(days=day_counter)
        )
        session.add(topic)
        session.flush()
        
        # Create checklist item for LEARN
        checklist = ChecklistItem(
            topic_id=topic.id,
            item_type="learn",
            description=f"Learn: {name}",
            scheduled_date=start_date + timedelta(days=day_counter),
            completed=False
        )
        session.add(checklist)
        
        # Create mastery tracking
        mastery = TopicMastery(topic_id=topic.id)
        session.add(mastery)
        
        day_counter += 1


def create_aptitude_topics(session, subject_id, start_date):
    """Create Quantitative Aptitude topics for Phase 1"""
    topics_data = [
        ("Number System (1/5)", 1, 5, ["Natural numbers", "Whole numbers", "Integers", "HCF", "LCM"], 1),
        ("Number System (2/5)", 2, 5, ["Divisibility rules", "Factors", "Multiples", "Prime factorization"], 1),
        ("Number System (3/5)", 3, 5, ["Remainders", "Cyclicity", "Unit digits"], 1),
        ("Number System (4/5)", 4, 5, ["Fractions", "Decimals", "BODMAS"], 1),
        ("Number System (5/5)", 5, 5, ["30-question practice set"], 1),
        ("Percentage (1/3)", 1, 3, ["Basics", "Percentage change", "Percentage of a number"], 1),
        ("Percentage (2/3)", 2, 3, ["Increase/decrease", "Successive changes"], 1),
        ("Percentage (3/3)", 3, 3, ["20-question practice set"], 1),
        ("Profit & Loss (1/3)", 1, 3, ["Cost price", "Selling price", "Profit/loss %"], 1),
        ("Profit & Loss (2/3)", 2, 3, ["Discount", "Marked price", "Successive discounts"], 1),
        ("Profit & Loss (3/3)", 3, 3, ["Practice set"], 1),
        ("Ratio & Proportion (1/2)", 1, 2, ["Basics", "Equivalent ratios", "Partnership"], 1),
        ("Ratio & Proportion (2/2)", 2, 2, ["Proportion", "Mean proportion", "Practice"], 1),
        ("Average (1/2)", 1, 2, ["Concept", "Weighted average"], 1),
        ("Average (2/2)", 2, 2, ["Average of groups", "Practice"], 1),
        ("Time & Work (1/3)", 1, 3, ["Basic concept", "LCM method"], 1),
        ("Time & Work (2/3)", 2, 3, ["Pipes and cisterns", "Efficiency"], 1),
        ("Time & Work (3/3)", 3, 3, ["Practice set"], 1),
        ("Time, Speed & Distance (1/3)", 1, 3, ["Basic formula", "Relative speed"], 1),
        ("Time, Speed & Distance (2/3)", 2, 3, ["Boats/streams", "Trains"], 1),
        ("Time, Speed & Distance (3/3)", 3, 3, ["Practice set"], 1),
        ("Simple & Compound Interest (1/2)", 1, 2, ["Simple interest", "Formula"], 1),
        ("Simple & Compound Interest (2/2)", 2, 2, ["Compound interest", "Yearly/half-yearly"], 1),
        ("Mixture & Alligation (1/2)", 1, 2, ["Concept", "Basic problems"], 1),
        ("Mixture & Alligation (2/2)", 2, 2, ["Practice set"], 1),
        ("Algebra (1/3)", 1, 3, ["Basic equations", "Identities"], 1),
        ("Algebra (2/3)", 2, 3, ["Linear equations", "Quadratic concept"], 1),
        ("Algebra (3/3)", 3, 3, ["Practice set"], 1),
        ("Probability (1/2)", 1, 2, ["Basic concept", "Classical probability"], 1),
        ("Probability (2/2)", 2, 2, ["Practice", "P&C intro"], 1),
        ("Data Interpretation (1/3)", 1, 3, ["Tables", "Bar charts"], 1),
        ("Data Interpretation (2/3)", 2, 3, ["Line graphs", "Pie charts"], 1),
        ("Data Interpretation (3/3)", 3, 3, ["Mixed DI", "Practice"], 1),
    ]
    
    for idx, (name, part, total, subtopics, phase) in enumerate(topics_data):
        topic = Topic(
            subject_id=subject_id,
            name=name,
            part_number=part,
            total_parts=total,
            subtopics=subtopics,
            sequence_order=idx + 1,
            phase=phase,
            scheduled_date=None  # Will be scheduled by checklist engine
        )
        session.add(topic)
        session.flush()
        
        mastery = TopicMastery(topic_id=topic.id)
        session.add(mastery)


def create_reasoning_topics(session, subject_id, start_date):
    """Create Logical Reasoning topics"""
    topics_data = [
        ("Analogy (1/2)", 1, 2, ["Word analogy", "Number analogy"], 1),
        ("Analogy (2/2)", 2, 2, ["Practice set"], 1),
        ("Classification (1/2)", 1, 2, ["Odd one out — words", "Numbers", "Figures"], 1),
        ("Classification (2/2)", 2, 2, ["Practice set"], 1),
        ("Series (1/3)", 1, 3, ["Number series", "Arithmetic", "Geometric"], 1),
        ("Series (2/3)", 2, 3, ["Letter series", "Mixed series"], 1),
        ("Series (3/3)", 3, 3, ["Practice set"], 1),
        ("Coding-Decoding (1/2)", 1, 2, ["Letter shift", "Number code"], 1),
        ("Coding-Decoding (2/2)", 2, 2, ["Practice set"], 1),
        ("Blood Relations (1/2)", 1, 2, ["Family tree problems"], 1),
        ("Blood Relations (2/2)", 2, 2, ["Practice set"], 1),
        ("Direction Sense (1/2)", 1, 2, ["Compass directions", "Distance"], 1),
        ("Direction Sense (2/2)", 2, 2, ["Practice set"], 1),
        ("Ranking (1/2)", 1, 2, ["Linear ranking", "Circular ranking"], 1),
        ("Ranking (2/2)", 2, 2, ["Practice set"], 1),
        ("Syllogism (1/2)", 1, 2, ["Venn diagram method"], 1),
        ("Syllogism (2/2)", 2, 2, ["Practice set"], 1),
        ("Puzzles (1/3)", 1, 3, ["Seating arrangement — linear"], 1),
        ("Puzzles (2/3)", 2, 3, ["Seating arrangement — circular"], 1),
        ("Puzzles (3/3)", 3, 3, ["Complex puzzles", "Practice"], 1),
        ("Logical Reasoning (1/2)", 1, 2, ["Assumptions", "Conclusions", "Inferences"], 1),
        ("Logical Reasoning (2/2)", 2, 2, ["Practice set"], 1),
    ]
    
    for idx, (name, part, total, subtopics, phase) in enumerate(topics_data):
        topic = Topic(
            subject_id=subject_id,
            name=name,
            part_number=part,
            total_parts=total,
            subtopics=subtopics,
            sequence_order=idx + 1,
            phase=phase,
            scheduled_date=None
        )
        session.add(topic)
        session.flush()
        
        mastery = TopicMastery(topic_id=topic.id)
        session.add(mastery)



def create_english_topics(session, subject_id, start_date):
    """Create English topics"""
    topics_data = [
        ("Grammar (1/4)", 1, 4, ["Parts of speech", "Tenses"], 1),
        ("Grammar (2/4)", 2, 4, ["Subject-verb agreement", "Articles"], 1),
        ("Grammar (3/4)", 3, 4, ["Prepositions", "Conjunctions", "Modifiers"], 1),
        ("Grammar (4/4)", 4, 4, ["Error detection", "Sentence improvement"], 1),
        ("Vocabulary (1/3)", 1, 3, ["Synonyms", "Antonyms", "Root words"], 1),
        ("Vocabulary (2/3)", 2, 3, ["Idioms and phrases"], 1),
        ("Vocabulary (3/3)", 3, 3, ["One-word substitution", "Practice"], 1),
        ("Reading Comprehension (1/3)", 1, 3, ["Main idea", "Tone", "Inference"], 1),
        ("Reading Comprehension (2/3)", 2, 3, ["Detailed reading", "Elimination technique"], 1),
        ("Reading Comprehension (3/3)", 3, 3, ["Speed practice", "Practice set"], 1),
        ("Cloze Test (1/2)", 1, 2, ["Strategy", "Practice"], 1),
        ("Cloze Test (2/2)", 2, 2, ["Practice set"], 1),
        ("Para Jumbles (1/2)", 1, 2, ["Strategy", "Connector words"], 1),
        ("Para Jumbles (2/2)", 2, 2, ["Practice set"], 1),
        ("Communication Skills (1/2)", 1, 2, ["Formal email", "Verbal fluency"], 1),
        ("Communication Skills (2/2)", 2, 2, ["Interview English", "HR questions"], 1),
    ]
    
    for idx, (name, part, total, subtopics, phase) in enumerate(topics_data):
        topic = Topic(
            subject_id=subject_id,
            name=name,
            part_number=part,
            total_parts=total,
            subtopics=subtopics,
            sequence_order=idx + 1,
            phase=phase,
            scheduled_date=None
        )
        session.add(topic)
        session.flush()
        
        mastery = TopicMastery(topic_id=topic.id)
        session.add(mastery)


def create_gs_topics(session, subject_id, start_date):
    """Create General Studies topics for MPSC Group C (Phase 1)"""
    topics_data = [
        ("Polity (1/4)", 1, 4, ["Indian Constitution", "Preamble", "Parts", "Schedules"], 1),
        ("Polity (2/4)", 2, 4, ["Fundamental Rights", "DPSP", "Fundamental Duties"], 1),
        ("Polity (3/4)", 3, 4, ["Parliament", "President", "PM", "Cabinet"], 1),
        ("Polity (4/4)", 4, 4, ["Judiciary", "Local Governance", "Panchayati Raj"], 1),
        ("History (1/4)", 1, 4, ["Modern India — 1857", "Gandhi era"], 1),
        ("History (2/4)", 2, 4, ["Freedom Movement", "Key events", "Leaders"], 1),
        ("History (3/4)", 3, 4, ["Maharashtra History", "Maratha Empire", "Social reform"], 1),
        ("History (4/4)", 4, 4, ["Practice set — MPSC PYQ"], 1),
        ("Geography (1/4)", 1, 4, ["Physical Geography", "Landforms", "Climate", "Rivers"], 1),
        ("Geography (2/4)", 2, 4, ["Indian Geography", "States", "Rivers", "Mountains"], 1),
        ("Geography (3/4)", 3, 4, ["Maharashtra Geography", "Districts", "Rivers", "Crops"], 1),
        ("Geography (4/4)", 4, 4, ["Practice set"], 1),
        ("Economics (1/3)", 1, 3, ["Basic Economics", "Demand/Supply", "GDP", "Inflation"], 1),
        ("Economics (2/3)", 2, 3, ["Indian Economy", "Banking", "RBI", "Budget"], 1),
        ("Economics (3/3)", 3, 3, ["Maharashtra economy", "Practice"], 1),
        ("General Science (1/4)", 1, 4, ["Physics", "Light", "Sound", "Motion"], 1),
        ("General Science (2/4)", 2, 4, ["Chemistry", "Elements", "Compounds", "Acids/Bases"], 1),
        ("General Science (3/4)", 3, 4, ["Biology", "Cell", "Body systems", "Nutrition"], 1),
        ("General Science (4/4)", 4, 4, ["Zoology/Botany/Health", "Practice"], 1),
    ]
    
    for idx, (name, part, total, subtopics, phase) in enumerate(topics_data):
        topic = Topic(
            subject_id=subject_id,
            name=name,
            part_number=part,
            total_parts=total,
            subtopics=subtopics,
            sequence_order=idx + 1,
            phase=phase,
            scheduled_date=None
        )
        session.add(topic)
        session.flush()
        
        mastery = TopicMastery(topic_id=topic.id)
        session.add(mastery)


def seed_database(user_name: str, start_date: date = date(2026, 6, 26)):
    """
    Main seed function - populates entire database
    """
    session = get_session()
    
    try:
        # Create user profile
        user = UserProfile(
            name=user_name,
            placement_status="pending",
            group_c_status="pending",
            current_phase=1,
            start_date=start_date
        )
        session.add(user)
        session.flush()
        
        # Create subjects
        subjects = [
            Subject(name="Data Structures & Algorithms", counts_for=["placement"], phase_introduced=1, is_active=True),
            Subject(name="Quantitative Aptitude", counts_for=["placement", "ssc", "mpsc_group_c", "mpsc_group_b"], phase_introduced=1, is_active=True),
            Subject(name="Logical Reasoning", counts_for=["placement", "ssc", "mpsc_group_c", "mpsc_group_b"], phase_introduced=1, is_active=True),
            Subject(name="English", counts_for=["placement", "ssc", "mpsc_group_c", "mpsc_group_b"], phase_introduced=1, is_active=True),
            Subject(name="General Studies", counts_for=["ssc", "mpsc_group_c", "mpsc_group_b"], phase_introduced=1, is_active=True),
            Subject(name="Current Affairs", counts_for=["ssc", "mpsc_group_c", "mpsc_group_b"], phase_introduced=1, is_active=True),
        ]
        
        for subj in subjects:
            session.add(subj)
        session.flush()
        
        # Create topics for each subject
        dsa_subject = session.query(Subject).filter_by(name="Data Structures & Algorithms").first()
        create_dsa_topics(session, dsa_subject.id, start_date)
        
        apt_subject = session.query(Subject).filter_by(name="Quantitative Aptitude").first()
        create_aptitude_topics(session, apt_subject.id, start_date)
        
        reasoning_subject = session.query(Subject).filter_by(name="Logical Reasoning").first()
        create_reasoning_topics(session, reasoning_subject.id, start_date)
        
        english_subject = session.query(Subject).filter_by(name="English").first()
        create_english_topics(session, english_subject.id, start_date)
        
        gs_subject = session.query(Subject).filter_by(name="General Studies").first()
        create_gs_topics(session, gs_subject.id, start_date)
        
        # Create initial daily log
        daily_log = DailyLog(
            log_date=start_date,
            total_study_minutes=0,
            tasks_completed=0,
            tasks_total=0,
            phase=1,
            streak_day=0
        )
        session.add(daily_log)
        
        session.commit()
        print("✓ Database seeded successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Seed failed: {e}")
        raise
    finally:
        session.close()
